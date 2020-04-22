from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import account.views
import account.views_inside
import chat.views

urlpatterns = [
    path('chat', account.views_inside.chat, name='chat'),
    path('play', account.views_inside.play, name='game-play'),
    path('characters', account.views_inside.list_characters, name= 'characters'),
    path('logout', account.views.do_logout, name='logout'),
    path('player-main', account.views_inside.player_main, name='player-main'),
    path('createacct', account.views.createacct, name='new-account'),
    path('login', account.views.do_login, name='login'),
    path('history', account.views_inside.history, name='game-history'),
    path('', account.views.index, name='index'),

    path('login/', account.views.do_login, name='login'),

]
