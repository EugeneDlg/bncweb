from time import time
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .models import Game

from .bnc_lib import get_new_guess_proposal, think_of_number_for_you


@login_required(login_url='login')
def home(request):
    if request.method == "POST":
        print("POST")
        try:
            game = Game.objects.get(game_id=request.session.session_key)
        except Exception:
            raise
    else:
        print("GET")
        try:
            game = Game.objects.get(game_id=request.session.session_key)
        except Game.DoesNotExist:
            game = Game.objects.create(
                game_id=request.session.session_key,
                # capacity=4,
                game_started=False,
                upper_poster="Please think of a number with 4 digits",
                attempts=0
            )
            game.save()
    return render(request, 'home.html', {'game': game})


@login_required(login_url='login')
def dual_game(request):
    if request.method == "POST":
        print("POST")
        try:
            game = Game.objects.get(game_id=request.session.session_key)
        except:
            raise
        if game.attempts == 0:
            game.my_guess = get_new_guess_proposal(game.capacity)
            game.my_number = think_of_number_for_you(game.capacity)
            game.attempts += 1
            game.start_timestamp = time()
            game.game_started = True
            game.upper_poster = "I wish you an interesting game!:-)"
            game.save()
            return render(request, 'dualgame.html', {'game': game})
        else:
            my_cows = request.POST["my_cows_"]
            my_bulls = request.POST["my_bulls_"]


    else:
        print("GET")
        try:
            game = Game.objects.get(game_id=request.session.session_key)
        except Exception:
            raise
        if game.attempts == 0:
            return redirect('home')
        # except Game.DoesNotExist:
        #     game = Game.objects.create(
        #         game_id=request.session.session_key,
        #         # capacity=4,
        #         game_started=False,
        #         attempts=0
        #     )
        #     game.save()
    return render(request, 'dualgame.html', {'game': game, 'upper_poster': upper_poster})


@login_required(login_url='login')
def single_game(request):
    return render(request, 'singlegame.html')
