from django.urls import path

import account.views

urlpatterns = [
    path('createacct', account.views.createacct, name='new-account'),
    path('login', account.views.do_login, name='login'),
    path('history', account.views.history, name='game-history'),
    path('', account.views.index, name='index'),

]