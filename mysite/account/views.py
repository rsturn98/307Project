# VIEWS RELATED TO LOGIN/LOGOUT/CREATE
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.conf import settings
import os
import stripe
from . import forms
from account.models import *
from chat import models as chatModels

# INDEX


def index(request):
    return render(request, "account/index.html")

# CREATE NEW ACCOUNT


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
    return render(request, 'account/createacct.html', context)

# LOGIN


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
                filterCharge = list(filter(lambda value: value.description == str(
                    request.user), stripe.Charge.list(limit=100)))
                if not filterCharge:  # payment
                    return HttpResponseRedirect('/pay/')
                if 'next' in request.GET:
                    return HttpResponseRedirect(request.GET['next'])
                # pass through character page
                return HttpResponseRedirect(reverse('characters'))
            else:
                form.add_error(None, 'Unable to log in')
        context['form'] = form
    return render(request, 'account/login.html', context)

# LOGOUT


def do_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
