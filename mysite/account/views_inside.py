# EVERYTHING ONCE YOU'VE LOGGED IN
from django.shortcuts import render
import stripe
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
from chat import models as chatModels

# GAME-PLAY CANVAS
@login_required
def play(request):
    filterChar = Character.objects.filter(user=request.user)
    myChar = filterChar[0]
    context = {'character': myChar.image_url}
    return render(request, "account/game-play.html", context)

# GO TO GAME
@login_required
def chat(request):
    return HttpResponseRedirect('/chat/')

# GAME-HISTORY
@login_required
def history(request):
    name = str(request.user.get_username())
    gameList = chatModels.Game.objects.filter(
        player1User=name) | chatModels.Game.objects.filter(player2User=name)
    countWins = gameList.filter(winner=name).count()
    countLosses = gameList.count() - countWins - gameList.filter(winner=None).count()
    context = {'battles': gameList,
               'user': name,
               'countWins': countWins,
               'countLosses': countLosses}  # EDIT -- needs to used database
    return render(request, "account/game-history.html", context)

# LIST CHARACTERS CHOICES
@login_required
def list_characters(request):
    context = {}
    filterChar = Character.objects.filter(user=request.user)
    if not filterChar:  # only set avatar once
        if request.method == 'POST':
            if 'choice' in request.POST:
                c = Character(
                    user=request.user,
                    image_url=request.POST['choice']
                )
                c.save()
                request.session['character'] = c.image_url
                return HttpResponseRedirect(reverse('player-main'))
        context = {'error_message': 'You must select a choice'}
        return render(request, 'account/characters.html', context)
    myChar = filterChar[0]
    request.session['character'] = myChar.image_url
    return HttpResponseRedirect(reverse('player-main'))

# MAIN SCREEN FOR PLAYERS
@login_required
def player_main(request):
    character = Character.objects.filter(user=request.user)[0].image_url
    context = {'user': request.user.username,
               'character': character}
    return render(request, 'account/player-main.html', context)
