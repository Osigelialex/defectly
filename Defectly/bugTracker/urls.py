from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('login', views.login_view, name='login'),
    path('home', views.home, name='home'),
    path('register', views.register, name='register'),
    path('logout', views.logout_view, name='logout')
]