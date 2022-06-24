import time
import math
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .models import Game, MyHistory, YourHistory, TotalSet, FixtureList

from .bnc_lib import get_my_first_guess, think_of_number_for_you, make_my_guess, validate_cows_and_bulls
from .bnc_lib import BnCException, validate_your_guess, make_your_guess, FinishedNotOKException


@login_required(login_url='login')
def home(request):
    if request.method == "POST":
        print("POST home")
        try:
            game = Game.objects.get(game_id=request.session.session_key)
        except Exception:
            raise
    else:
        print("GET home")
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
            my_history = MyHistory.objects.create(
                game_id=game
            )
            my_history.save()
            your_history = YourHistory.objects.create(
                game_id=game
            )
            your_history.save()
            total_set = TotalSet.objects.create(
                game_id=game
            )
            total_set.save()
        if game.attempts > 0:
            if game.dual_game:
                return redirect('dualgame')
            else:
                return redirect('singlegame')

    return render(request, 'home.html', {'game': game})


@login_required(login_url='login')
def dual_game(request):
    if request.method == "POST":
        print("POST dualgame")
        flag = int(request.POST.get("flag", False))
        # flag = request.POST["flag"]
        print(flag)
        try:
            game = Game.objects.get(game_id=request.session.session_key)
            my_history = MyHistory.objects.get(game_id=request.session.session_key)
            your_history = YourHistory.objects.get(game_id=request.session.session_key)
            total_set = TotalSet.objects.get(game_id=request.session.session_key)
        except:
            raise
        if game.attempts == 0:
            # if not flag:
            #     return JsonResponse({"is_OK": True})
            game.my_guess = get_my_first_guess(game.capacity)
            game.my_number = think_of_number_for_you(game.capacity)
            game.attempts += 1
            game.start_timestamp = time.time()
            game.game_started = True
            game.upper_poster = "I wish you an interesting game!:-)"
            game.save()
            return render(request, 'dualgame.html', {'game': game})
        else:
            if not flag:
                my_cows_entered = request.POST["my_cows"]
                my_bulls_entered = request.POST["my_bulls"]
                if game.dual_game:
                    your_guess_entered = request.POST["your_guess"]
                try:
                    validate_cows_and_bulls(my_cows_entered, my_bulls_entered, game.capacity)
                    validate_your_guess(game.capacity, your_guess_entered)
                    print("validate_cows_and_bulls")
                except BnCException as exc:
                    response = {"is_OK": False, "items": exc.msg}
                    return JsonResponse(response)
                except Exception as exc:
                    raise exc
                else:
                    game.my_cows = int(my_cows_entered)
                    game.my_bulls = int(my_bulls_entered)
                    game.your_guess = str(your_guess_entered)
                    game.save()
                    return JsonResponse({"is_OK": True})
            # result_code = None
            if my_history.items is None:
                game.my_history_list = []
            else:
                game.my_history_list = my_history.items
            if total_set.set is None:
                game.total_set = set()
            else:
                game.total_set = set(total_set.set)
            try:
                my_result = make_my_guess(game)
            except FinishedNotOKException as exc:
                game.result_code = 0
                game.save()
                finish_dual_game(game, 0)
                return render(request, 'dualgame.html', {'game': game})
            my_history.items = game.my_history_list
            my_history.save()
            total_set.set = list(game.total_set)
            total_set.save()
            del game.my_history_list
            del game.total_set
            if game.dual_game:
                if your_history.items is None:
                    game.your_history_list = []
                else:
                    game.your_history_list = your_history.items
                your_result = make_your_guess(game, game.your_guess)
                your_history.items = game.your_history_list
                your_history.save()
                del game.your_history_list
            else:
                your_result = False
            game.save()
            if my_result and not your_result:
                game.result_code = 1
            if your_result and not my_result:
                game.result_code = 2
            if your_result and my_result:
                game.result_code = 3
            if game.result_code is not None:
                finish_dual_game(request, game)
            return render(request, 'dualgame.html', {'game': game,
                                                     'my_items': my_history.items, 'your_items': your_history.items})
    else:
        print("GET dualgame")
        try:
            game = Game.objects.get(game_id=request.session.session_key)
            my_history = MyHistory.objects.get(game_id=request.session.session_key)
            your_history = YourHistory.objects.get(game_id=request.session.session_key)
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
    print("length of items: ", len(my_history.items))
    return render(request, 'dualgame.html', {'game': game,
                                             'my_items': my_history.items, 'your_items': your_history.items})


@login_required(login_url='login')
def single_game(request):
    return render(request, 'singlegame.html')


def home1(request):
    return render(request, 'singlegame.html')


def finish_dual_game(request, game):
    game.finish_timestamp = time.time()
    result_code = game.result_code
    game.game_started = False
    if result_code == 0:
        game.upper_poster = "You have broken my mind! Please be more careful! Think of a new number!"
    elif result_code == 1:
        game.upper_poster = "YAHOO! I've won! Thank you the for interesting game! " \
                                   "Attempts: " + str(game.attempts)
    elif result_code == 2:
        game.upper_poster = "Today is your day! You've won. Congrats! " \
                                   "Attempts: " + str(game.attempts)
    else:
        game.upper_poster = "We've ended this game in a tie... " \
                                   "Attempts: " + str(game.attempts)
    game.new_game_requested = True
    game.game_started = False
    game.my_guess = None
    game.your_guess = None
    game.save()
    if result_code > 0:
        write_fl_to_db(request, game)


def new_game(request):
    try:
        game = Game.objects.get(game_id=request.session.session_key)
        my_history = MyHistory.objects.get(game_id=request.session.session_key)
        your_history = YourHistory.objects.get(game_id=request.session.session_key)
        total_set = TotalSet.objects.get(game_id=request.session.session_key)
    except:
        raise
    my_history.items = []
    my_history.save()
    your_history.items = []
    your_history.save()
    total_set.set = []
    total_set.save()
    game.game_started = False
    game.new_game_requested = True
    game.my_bulls = None
    game.my_cows = None
    game.my_guess = None
    game.my_number = None
    game.your_bulls = None
    game.your_cows = None
    game.your_guess = None
    game.your_number = None
    game.capacity = 4
    game.attempts = 0
    game.available_digits_str = "0123456789"
    game.start_time = None
    game.finish_time = None
    game.upper_poster = "Please think of a number with 4 digits"
    # game.dual_game keeps the previous state
    game.save()
    return redirect('home')

#
# def fixture_list():

def write_fl_to_db(request, game):
    game = FixtureList.objects.create(
        username=request.user.username,
        winner=game.result_code,
        attempts=game.attempts,
        timestamp=game.start_timestamp,
        duration=math.ceil((game.finish_timestamp - game.start_timestamp) / 60)
    )
    game.save()