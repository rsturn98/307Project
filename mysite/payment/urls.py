from django.urls import path
from django.contrib.auth.decorators import login_required 
from . import views

urlpatterns = [
    path('account/', views.account, name='complete'),
    path('charge/', views.charge, name='charge'),
    path('', login_required(views.HomePageView.as_view()), name='home'),
]