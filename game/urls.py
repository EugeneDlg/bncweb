from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('dualgame.html', views.dual_game, name='dualgame'),
    path('singlegame.html', views.single_game, name='singlegame'),
]