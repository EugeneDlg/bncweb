from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [

    path('dualgame/', views.dual_game, name='dualgame'),
    path('singlegame.html', views.single_game, name='singlegame'),
    path('newgame', views.new_game, name="new_game"),
    path('fixturelist', views.fixture_list, name="fixture_list"),
    path('edit', views.edit_profile, name="edit"),
    path('changepassword', views.change_password, name="change_password"),
    path('delete', views.delete_profile, name="delete"),
    path('', views.home, name='home'),
]