from django.urls import path

import account.views

urlpatterns = [
    path('', account.views.index, name='index'),
    
]