from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [

    path('dualgame/', views.dual_game, name='dualgame'),
    path('singlegame.html', views.single_game, name='singlegame'),
    path('new_game', views.new_game, name="new_game"),
    path('fixturelist', views.fixture_list, name="fixture_list"),
    path('users', views.users_view, name="users"),
    path('', views.home, name='home'),
]