from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import account.views

urlpatterns = [
    path('play', account.views.play, name='game-play'),
    path('characters', account.views.list_characters, name= 'characters'),
    path('logout', account.views.do_logout, name='logout'),
    path('player-main', account.views.player_main, name='player-main'),
    path('createacct', account.views.createacct, name='new-account'),
    path('login', account.views.do_login, name='login'),
    path('history', account.views.history, name='game-history'),
    path('', account.views.index, name='index'),

]