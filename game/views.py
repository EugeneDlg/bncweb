from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .models import Game


@login_required(login_url='login')
def home(request):
    if request.method == "POST":
        print("POST")
    else:
        print("GET")
        try:
            game = Game.objects.get(game_id=request.session.session_key)
        except Game.DoesNotExist:
            game = Game.objects.create(
                game_id=request.session.session_key,
                # capacity=4,
                game_started=False
            )
            game.save()
    return render(request, 'home.html', {'game': game})
# return render(request, 'home.html', )
