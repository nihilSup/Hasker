from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.urls import reverse

from .forms import UserForm


def index(request):
    return render(request, 'hasker/index.html')


def signup(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            # to hash the password
            user.set_password(user.password)
            user.save()
            registered = True
        else:
            print(user_form.errors)
    else:
        # provide empty fields for new user registration
        user_form = UserForm()
    return render(request, 'hasker/signup.html',
                  dict(user_form=user_form, registered=registered))


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


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))
