from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.urls import reverse

from .forms import UserForm, UserProfileForm


def index(request):
    return render(request, 'hasker/index.html')


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


def profile(request):
    if request.method == 'POST':
        profile_form = UserProfileForm(data=request.POST,
                                       instance=request.user,
                                       files=request.FILES or None)
        if profile_form.is_valid():
            user_model = profile_form.save()
            user_model.save()
        else:
            print(profile_form.errors)
    else:
        profile_form = UserProfileForm(instance=request.user)
    return render(request, 'hasker/profile.html',
                  dict(profile_form=profile_form))
