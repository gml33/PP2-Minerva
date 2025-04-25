from django.urls import path
from .views import *

app_name = 'app'


urlpatterns = [
    path('',home,name=''),
    path('register',register, name='register'),
    path('my-login',my_login, name='my-login'),
    path('user-logout',user_logout, name='user-logout'),
    path('dashboard',dashboard, name='dashboard'),
    #------------------------periodico--------------------------------
    path('agregar-periodico', agregar_periodico, name='agregar_periodico'),
    #------------------------link-------------------------------------
    path('agregar-link', agregar_link, name='agregar_link'),
    ]