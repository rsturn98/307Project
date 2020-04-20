from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from account.models import *
from django.db import IntegrityError
from . import forms
import os
from django.conf import settings
from django.templatetags.static import static
from django.contrib.staticfiles.utils import get_files
from django.contrib.staticfiles.storage import StaticFilesStorage

# Create your views here.
def index(request):
    return render(request, "index.html")

def play(request):
    return render(request, "game-play.html")

#GAME-HISTORY
@login_required
def history(request):
    context = {'battles': ''} #EDIT -- needs to used database
    return render(request, "game-history.html")

#LIST CHARACTERS CHOICES
@login_required
def list_characters(request):
    if not Character.objects.filter(user=request.user):
        if request.method == 'POST':
            #add in form portion
            if 'choice' in request.POST:
                c = Character(
                    user = request.user,
                    image_url = request.POST['choice']
                )
                c.save()
                #myCharacter = Character.objects.cre
                return HttpResponseRedirect(reverse('player-main'))
        characters = []
        for c in os.listdir(os.path.join(settings.BASE_DIR, 'account', 'static', 'account')):
            if c.startswith('bard'):
                characters.append({
                    'image': c
                })
        context = {
            'characters': characters,
            'error_message': 'You must select a choice'
        }
        return render(request, 'characters.html', context)
    return HttpResponseRedirect(reverse('player-main'))

#MAIN SCREEN FOR PLAYERS
@login_required
def player_main(request):
    context = {'user':request.user.username}
    return render(request, 'player-main.html', context)

#CREATE NEW ACCOUNT
def createacct(request):
    context = {}
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            try:
              user = User.objects.create_user(
                form.cleaned_data['username'], 
                password=form.cleaned_data['password'])
              return HttpResponseRedirect(reverse('characters'))
              #return HttpResponseRedirect(reverse('login'))
            except IntegrityError:
                form.add_error('username', 'Username is taken')

        context['form'] = form   
    return render(request, 'createacct.html', context)

#LOGIN
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
                return HttpResponseRedirect(reverse('characters'))
            else:
                form.add_error(None, 'Unable to log in')
        context['form'] = form
    return render(request, 'login.html', context)

#LOGOUT
def do_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))