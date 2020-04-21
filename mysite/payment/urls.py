from django.urls import path

from . import views

urlpatterns = [
    path('account/', views.account, name='complete'),
    path('charge/', views.charge, name='charge'),
    path('', views.HomePageView.as_view(), name='home'),
]