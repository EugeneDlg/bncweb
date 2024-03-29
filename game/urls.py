from django.urls import path
from . import views


urlpatterns = [
    path('dualgame/', views.dual_game, name='dualgame'),
    path('singlegame/', views.single_game, name='singlegame'),
    path('fixturelist/', views.fixture_list, name="fixture_list"),
    path('settings/', views.settings, name="settings"),
    path('about/', views.about, name="about"),
    path('', views.home, name='home'),
]