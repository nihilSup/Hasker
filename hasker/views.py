from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib import auth
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.paginator import Paginator

from .forms import UserForm, UserProfileForm, QuestionForm
from .models import Question


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


@login_required(login_url='login')
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


@login_required(login_url='login')
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


@login_required(login_url='login')
def ask(request):
    if request.method == 'POST':
        q_form = QuestionForm(data=request.POST)
        if q_form.is_valid():
            q_model = q_form.save(commit=False)
            q_model.author = request.user
            q_model.asked_date = timezone.now()
            q_model.save()
            q_form.save_m2m()
        else:
            print(q_form.errors)
    else:
        q_form = QuestionForm()
    return render(request, 'hasker/ask.html',
                  dict(q_form=q_form))


def question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'hasker/question.html', dict(question=question))
