from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib import auth
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Count

import json

from .forms import UserForm, UserProfileForm, QuestionForm, AnswerForm
from .models import Question, Answer


def index(request):
    all_q = Question.objects.order_by('-asked_date')
    paginator = Paginator(all_q, 4)
    page = request.GET.get('page')
    questions = paginator.get_page(page)
    return render(request, 'hasker/index.html', dict(questions=questions))


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)

        if user:
            if user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse('Account is disabled.')
        else:
            print('Invalid login/pass'.format(username, password))
            return HttpResponse('Invalid login/pass')
    else:
        return render(request, 'hasker/login.html')


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


def signup(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            if(user_form.cleaned_data['password'] !=
               user_form.cleaned_data['password_re']):
                user_form.add_error('password', 'Passwords do not match')
                print(user_form.errors)
            else:
                user = user_form.save()
                # to hash the password
                user.set_password(user.password)
                if 'avatar' in request.FILES:
                    user.avatar = request.FILES['avatar']
                user.save()
                registered = True
        else:
            print(user_form.errors)
    else:
        # provide empty fields for new user registration
        user_form = UserForm()
    return render(request, 'hasker/signup.html',
                  dict(user_form=user_form, registered=registered))


@login_required
def profile(request):
    if request.method == 'POST':
        profile_form = UserProfileForm(data=request.POST,
                                       instance=request.user,
                                       files=request.FILES or None)
        if profile_form.is_valid():
            user_model = profile_form.save()
        else:
            print(profile_form.errors)
    else:
        profile_form = UserProfileForm(instance=request.user)
    return render(request, 'hasker/profile.html',
                  dict(profile_form=profile_form))


@login_required
def ask(request):
    if request.method == 'POST':
        q_form = QuestionForm(data=request.POST)
        if q_form.is_valid():
            q_model = q_form.save(commit=False)
            q_model.author = request.user
            q_model.asked_date = timezone.now()
            q_model.save()
            q_form.save_m2m()
            return redirect('question', question_id=q_model.id)
        else:
            print(q_form.errors)
    else:
        q_form = QuestionForm()
    return render(request, 'hasker/ask.html',
                  dict(q_form=q_form))


def question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        add_answer_form = AnswerForm(request.POST)
        if add_answer_form.is_valid():
            answer_model = add_answer_form.save(commit=False)
            answer_model.question = question
            answer_model.author = request.user
            answer_model.answered_date = timezone.now()
            answer_model.is_correct = False
            answer_model.save()
        else:
            print(add_answer_form.errors)
    else:
        add_answer_form = AnswerForm()
    answers = (
        Answer.objects.filter(question=question)
        .order_by('-votes', '-answered_date')
    )
    return render(request, 'hasker/question.html',
                  dict(question=question, answers=answers,
                       add_answer_form=add_answer_form))


def process_vote(obj, request):
    user_ups = obj.up_votes.filter(id=request.user.id).count()
    user_downs = obj.down_votes.filter(id=request.user.id).count()
    if request.method == 'POST' and request.user.is_authenticated:
        if request.POST['vote_type'] == 'up':
            if user_ups == 0 and user_downs == 0:
                obj.up_votes.add(request.user)
                obj.save()
            elif user_ups == 0 and user_downs != 0:
                obj.down_votes.remove(request.user)
                obj.save()
        if request.POST['vote_type'] == 'down':
            if user_ups == 0 and user_downs == 0:
                obj.down_votes.add(request.user)
                obj.save()
            elif user_ups != 0 and user_downs == 0:
                obj.up_votes.remove(request.user)
                obj.save()
    return HttpResponse(json.dumps(dict(
        user_ups=obj.up_votes.filter(id=request.user.id).count(),
        user_downs=obj.down_votes.filter(id=request.user.id).count(),
        votes=(obj.votes)
    )))


def question_votes(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return process_vote(question, request)


def answer_votes(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    return process_vote(answer, request)
