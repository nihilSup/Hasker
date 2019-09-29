import json
import logging
import re

from django.conf import settings
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.http import (Http404, HttpResponse, HttpResponseRedirect,
                         JsonResponse)
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DetailView
from django.views.generic.detail import SingleObjectMixin

from .forms import AnswerForm, QuestionForm, UserForm, UserProfileForm
from .models import Answer, Question, Tag

logger = logging.getLogger(__name__)




def index(request):
    field_name = request.GET.get('sortby')
    if field_name not in ('-asked_date', '-votes'):
        field_name = '-asked_date'
    all_q = Question.objects.order_by(field_name)
    paginator = Paginator(all_q, 4)
    page = request.GET.get('page')
    questions = paginator.get_page(page)
    return render(request, 'hasker/index.html', dict(questions=questions,
                                                     sortedby=field_name))


def login(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)

        if user:
            if user.is_active:
                auth.login(request, user)
                return redirect('index')
            else:
                logger.info('User deactivated')
                error = 'User deactivated'
        else:
            logger.info('Invalid login/pass')
            error = 'Invalid login/pass'
    return render(request, 'hasker/login.html', dict(error=error))


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


def signup(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            # to hash the password
            user.set_password(user.password)
            if 'avatar' in request.FILES:
                user.avatar = request.FILES['avatar']
            user.save()
            registered = True
        else:
            logger.info(user_form.errors)
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
            logger.info(profile_form.errors)
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
            # TODO: should I move code below to Tag model?
            for tag_name in q_form.cleaned_data['tags']:
                tag = Tag.objects.filter(name=tag_name).first()
                if tag is None:
                    q_model.tags.create(name=tag_name)
                else:
                    q_model.tags.add(tag)
            return redirect('question', question_id=q_model.id)
        else:
            logger.info(q_form.errors)
    else:
        q_form = QuestionForm()
    return render(request, 'hasker/ask.html',
                  dict(q_form=q_form))


class QuestionDetails(DetailView):
    model = Question
    template_name = 'hasker/question.html'
    pk_url_kwarg = 'question_id'
    context_object_name = 'question'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question = self.get_object()
        answers = (
            Answer.objects.filter(question=question)
            .order_by('-votes', '-answered_date')
        )
        corr_answer = any(answer.is_correct for answer in answers)

        paginator = Paginator(answers, 4)
        page = self.request.GET.get('page')
        answers = paginator.get_page(page)
        add_answer_form = AnswerForm()
        context.update(dict(answers=answers,
                            add_answer_form=add_answer_form,
                            corr_answer=corr_answer))
        return context

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        question = self.get_object()
        add_answer_form = AnswerForm(request.POST)
        if add_answer_form.is_valid():
            answer_model = add_answer_form.save(commit=False)
            answer_model.question = question
            answer_model.author = request.user
            answer_model.answered_date = timezone.now()
            answer_model.is_correct = False
            answer_model.save()
            link = request.build_absolute_uri()
            send_mail(
                'You have a new answer!',
                f'Hi, check new answer to {link}',
                settings.EMAIL_HOST_USER,
                [question.author.email],
                fail_silently=True,
            )
        else:
            logger.info(add_answer_form.errors)
        self.object = question
        context = self.get_context_data()
        context['form'] = add_answer_form
        return self.render_to_response(context)


class BaseVotesView(View, SingleObjectMixin):
    def as_json_resp(self, obj, request):
        return JsonResponse(dict(
            user_ups=obj.user_ups(request.user),
            user_downs=obj.user_downs(request.user),
            votes=(obj.votes)
        ))

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        return self.as_json_resp(obj, request)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.handle_new_vote(request.user, request.POST['vote_type'])
        return self.as_json_resp(obj, request)



class QuestionVotesView(BaseVotesView):
    model = Question
    pk_url_kwarg = 'question_id'


class AnswerVotesView(BaseVotesView):
    model = Answer
    pk_url_kwarg = 'answer_id'


@login_required
def select_answer(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.method == 'POST' and request.user == answer.question.author:
        answer.is_correct = json.loads(request.POST['is_correct'])
        answer.save(update_fields=["is_correct"])
    return HttpResponse('Ok')


def search(request):
    query = request.GET.get('search_query')
    questions = Question.search(query)
    paginator = Paginator(questions, 4)
    page = request.GET.get('page')
    questions = paginator.get_page(page)
    return render(request, 'hasker/search.html', dict(questions=questions,
                                                      search_query=query))
