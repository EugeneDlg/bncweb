from time import time
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .models import Game, MyHistory, YourHistory, TotalSet, CurrentSet

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
            current_set = CurrentSet.objects.create(
                game_id=game
            )
            current_set.save()
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
            game.start_timestamp = time()
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
                    game.your_guess = int(your_guess_entered)
                    game.save()
                    return JsonResponse({"is_OK": True})

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
                finish_dual_game(0)
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
            return render(request, 'dualgame.html', {'game': game, 'result_code': None})
    else:
        print("GET dualgame")
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
    return render(request, 'dualgame.html', {'game': game})


@login_required(login_url='login')
def single_game(request):
    return render(request, 'singlegame.html')


def validate_game_data(request):
    return render(request, 'singlegame.html')
    # my_cows = request.GET.get('my_cows_', None)
    # print("validate my cows")
    # response = {
    #     'is_correct': False
    # }
    # return JsonResponse(response)


def home1(request):
    return render(request, 'singlegame.html')


def finish_dual_game(request, game, result_code):
    # game.finish_timestamp = time()
    game.game_started = False
    if result_code == 0:
        game.upper_label = "You have broken my mind! Please be more carefull! Think of a new number!"
    elif result_code == 1:
        game.upper_label = "YAHOO! I've won! Thank you the for interesting game!" \
                                   "Attempts: " + str(game.attempts)
    elif result_code == 2:
        game.upper_label = "Today is your day! You've won! Congrats!" \
                                   "Attempts: " + str(game.attempts)
    else:
        game.upper_label = "We've ended this game in a tie!.." \
                                   "Attempts: " + str(game.attempts)
    game.new_game_requested = True
    # add_item_to_my_and_your_history_frame()
    # if result_code > 0:
    #     write_fl_to_db(game, result_code)
    return render(request, 'dualgame.html', {'game': game, 'result_code': result_code})


