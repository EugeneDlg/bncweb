from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('dualgame/', views.dual_game, name='dualgame'),
    path('singlegame.html', views.single_game, name='singlegame'),
    # path('', views.validate_game_data, name='validate_game_data'),
]