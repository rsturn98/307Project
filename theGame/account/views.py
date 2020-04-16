from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from account.models import *
from django.db import IntegrityError
from . import forms

# Create your views here.
def index(request):
    return render(request, "index.html")

@login_required
def history(request):
    return render(request, "game-history.html")

@login_required
def list_characters(request):
    characters = []
    for c in Character.objects.all():
        characters.append({
            'image_url': c.image_url
        })
    context = {'characters': characters}
    return render(request, 'characters.html', context)

def createacct(request):
    context = {}
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            try:
              user = User.objects.create_user(
                form.cleaned_data['username'], 
                password=form.cleaned_data['password'])
              return HttpResponseRedirect(reverse('login'))
            except IntegrityError:
                form.add_error('username', 'Username is taken')

        context['form'] = form   
    return render(request, 'createacct.html', context)

def do_login(request):
    context = {}
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, 
              username=form.cleaned_data['username'], 
              password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                if 'next' in request.GET:
                    return HttpResponseRedirect(request.GET['next'])
                return HttpResponseRedirect(reverse('acc_info'))
            else:
                form.add_error(None, 'Unable to log in')
        context['form'] = form
    return render(request, 'login.html', context)

def do_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))