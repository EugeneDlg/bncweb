import datetime as dt
import math

from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from jsonview.decorators import json_view
from crispy_forms.utils import render_crispy_form

from bncutils.bnc_lib import get_my_first_guess, think_of_number_for_you, make_my_guess, validate_cows_and_bulls
from bncutils.bnc_lib import BnCException, validate_your_guess, make_your_guess, FinishedNotOKException
from bncutils.bnc_lib import get_data_for_fixture_table, read_config, read_phrases

from .models import Game, MyHistory, YourHistory, TotalSet, FixtureList
from .forms import SettingsForm


initial_settings = read_config()
# good_phrases = read_phrases()
initial_single_phrase = "Please think of a number with ___ digits."
initial_dual_phrase = " And I will think of a number (___ digits) for you."
default_game_phrase = "I wish you an interesting game!:-)"
broken_game_phrase = "You have broken my mind! Please be more careful! Think of a new number!"


@login_required(login_url='login')
def home(request):
    if request.method == "POST":
        game = Game.objects.get(user=request.user)
    else:
        try:
            game = Game.objects.get(user=request.user)
            if game.attempts > 0:
                if game.dual_game:
                    return redirect('dualgame')
                else:
                    return redirect('singlegame')
            game.upper_poster = initial_single_phrase.replace("___", str(game.capacity))
            if game.dual_game:
                game.upper_poster += initial_dual_phrase.replace("___", str(game.capacity))
            game.save()
        except Game.DoesNotExist:
            upper_poster = initial_single_phrase.replace("___", str(initial_settings["default_capacity"]))
            # dual game is enabled by default
            upper_poster += initial_dual_phrase.replace("___", str(initial_settings["default_capacity"]))  
            game = Game.objects.create(
                game_id=request.session.session_key,
                upper_poster=upper_poster,
                capacity=initial_settings["default_capacity"],
                user=request.user
            )
            MyHistory.objects.create(
                game_id=game
            )
            YourHistory.objects.create(
                game_id=game
            )
            TotalSet.objects.create(
                game_id=game
            )
    return render(request, 'home.html', {'game': game})


@login_required(login_url='login')
def dual_game(request):
    if request.method == "POST":
        submit_flag = bool(int(request.POST.get("flag", False)))
        game = Game.objects.get(user=request.user)
        my_history = MyHistory.objects.get(game_id=game.game_id)
        your_history = YourHistory.objects.get(game_id=game.game_id)
        total_set = TotalSet.objects.get(game_id=game.game_id)
        if game.attempts == 0:
            game.my_number = think_of_number_for_you(game.capacity)
            attempt_zero(game)
            return render(request, 'dualgame.html', {'game': game})
        else:
            if game.new_game_requested:
                reset_to_initials(game)
                return redirect('home')
            finished_flag = bool(int(request.POST.get("finished_flag", False)))
            if finished_flag:
                reset_to_initials(game)
                game.save()
                return redirect('home')
            if not submit_flag:
                my_cows_entered = request.POST["my_cows"]
                my_bulls_entered = request.POST["my_bulls"]
                your_guess_entered = request.POST["your_guess"]
                try:
                    validate_cows_and_bulls(my_cows_entered, my_bulls_entered, game.capacity)
                    validate_your_guess(game.capacity, your_guess_entered)
                except BnCException as exc:
                    response = {"success": False, "items": exc.msg}
                    return JsonResponse(response)
                else:
                    game.my_cows = int(my_cows_entered)
                    game.my_bulls = int(my_bulls_entered)
                    game.your_guess = str(your_guess_entered)
                    game.save()
                    return JsonResponse({"success": True})
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
                finish_dual_game(request, game)
                return render(request, 'dualgame.html', {'game': game})
            my_history.items = game.my_history_list
            my_history.save()
            total_set.set = list(game.total_set)
            total_set.save()
            del game.my_history_list
            del game.total_set
            if your_history.items is None:
                game.your_history_list = []
            else:
                game.your_history_list = your_history.items
            your_result = make_your_guess(game, game.your_guess)
            your_history.items = game.your_history_list
            your_history.save()
            del game.your_history_list
            if my_result and not your_result:
                game.result_code = 1
            if your_result and not my_result:
                game.result_code = 2
            if your_result and my_result:
                game.result_code = 3
            game.elapsed = int(timezone.now().timestamp() - game.start_time.timestamp())
            game.save()
            if game.result_code is not None:
                finish_dual_game(request, game)
            return render(request, 'dualgame.html', {'game': game,
                                                     'my_items': my_history.items, 'your_items': your_history.items})
    else:
        # create_user_privileges(request)
        try:
            game = Game.objects.get(user=request.user)
            my_history = MyHistory.objects.get(game_id=game.game_id)
            your_history = YourHistory.objects.get(game_id=game.game_id)
        except Game.DoesNotExist:
            upper_poster = initial_single_phrase.replace("___", str(initial_settings["default_capacity"]))
            # dual game is enabled by default
            upper_poster += initial_dual_phrase.replace("___", str(initial_settings["default_capacity"]))  
            game = Game.objects.create(
                game_id=request.session.session_key,
                game_started=False,
                upper_poster=upper_poster,
                capacity=initial_settings["default_capacity"],
                attempts=0
            )
        if game.attempts == 0:
            return redirect('home')
    if game.game_started:
        game.elapsed = int(timezone.now().timestamp() - game.start_time.timestamp())
        game.save()
    return render(request, 'dualgame.html', {'game': game,
                                             'my_items': my_history.items, 'your_items': your_history.items})


@login_required(login_url='login')
def single_game(request):
    if request.method == "POST":
        submit_flag = bool(int(request.POST.get("flag", False)))
        game = Game.objects.get(user=request.user)
        my_history = MyHistory.objects.get(game_id=game.game_id)
        total_set = TotalSet.objects.get(game_id=game.game_id)
        if game.attempts == 0:
            attempt_zero(game)
            return render(request, 'singlegame.html', {'game': game})
        else:
            if game.new_game_requested:
                reset_to_initials(game)
                return redirect('home')
            finished_flag = bool(int(request.POST.get("finished_flag", False)))
            if finished_flag:
                reset_to_initials(game)
                game.save()
                return redirect('home')
            if not submit_flag:
                my_cows_entered = request.POST["my_cows"]
                my_bulls_entered = request.POST["my_bulls"]
                try:
                    validate_cows_and_bulls(my_cows_entered, my_bulls_entered, game.capacity)
                except BnCException as exc:
                    response = {"success": False, "items": exc.msg}
                    return JsonResponse(response)
                else:
                    game.my_cows = int(my_cows_entered)
                    game.my_bulls = int(my_bulls_entered)
                    game.save()
                    return JsonResponse({"success": True})
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
                finish_single_game(request, game)
                return render(request, 'singlegame.html', {'game': game})
            my_history.items = game.my_history_list
            my_history.save()
            total_set.set = list(game.total_set)
            total_set.save()
            del game.my_history_list
            del game.total_set
            if my_result:
                game.result_code = 1
            game.elapsed = int(timezone.now().timestamp() - game.start_time.timestamp())
            game.save()
            if game.result_code is not None:
                finish_single_game(request, game)
            return render(request, 'singlegame.html', {'game': game,
                                                       'my_items': my_history.items})
    else:
        try:
            game = Game.objects.get(user=request.user)
            my_history = MyHistory.objects.get(game_id=game.game_id)
        except Game.DoesNotExist:
            game = Game.objects.create(
                game_id=request.session.session_key,
                game_started=False,
                upper_poster=initial_single_phrase.replace("___", str(initial_settings["default_capacity"])),
                capacity=initial_settings["default_capacity"],
                attempts=0
            )
        if game.attempts == 0:
            return redirect('home')
    if game.game_started:
        game.elapsed = int(timezone.now().timestamp() - game.start_time.timestamp())
        game.save()
    return render(request, 'singlegame.html', {'game': game,
                                               'my_items': my_history.items})


def attempt_zero(game):
    game.my_guess = get_my_first_guess(game.capacity)
    game.attempts += 1
    game.start_time = timezone.now()
    game.game_started = True
    game.new_game_requested = False
    game.upper_poster = default_game_phrase
    # game.upper_poster = choice(good_phrases)
    game.result_code = None
    game.elapsed = 0
    game.save()

def finish_dual_game(request, game):
    result_code = game.result_code
    game.finish_time = timezone.now()
    game.elapsed = int(game.finish_time.timestamp() - game.start_time.timestamp())
    game.game_started = False
    game.new_game_requested = True
    if result_code == 0:
        game.upper_poster = broken_game_phrase
    elif result_code == 1:
        game.upper_poster = "YAHOO! I've won! Thank you the for interesting game! " \
                            "Attempts: " + str(game.attempts)
    elif result_code == 2:
        game.upper_poster = "Today is your day! You've won. Congrats! " \
                            "Attempts: " + str(game.attempts)
    else:
        game.upper_poster = "We've ended this game in a tie... " \
                            "Attempts: " + str(game.attempts)
    game.save()
    if result_code > 0:
        write_fl_to_db(request, game)


def finish_single_game(request, game):
    result_code = game.result_code
    game.finish_time = timezone.now()
    game.elapsed = int(game.finish_time.timestamp() - game.start_time.timestamp())
    game.game_started = False
    game.new_game_requested = True
    if result_code == 0:
        game.upper_poster = broken_game_phrase
    elif result_code == 1:
        game.upper_poster = "YAHOO! I've won! Thank you the for interesting game! " \
                            "Attempts: " + str(game.attempts)
    game.save()


def reset_to_initials(game):
    my_history = MyHistory.objects.get(game_id=game.game_id)
    my_history.items = []
    my_history.save()
    upper_poster = initial_single_phrase.replace("___", str(game.capacity))
    if game.dual_game:
        your_history = YourHistory.objects.get(game_id=game.game_id)
        your_history.items = []
        your_history.save()
        upper_poster += initial_dual_phrase.replace("___", str(game.capacity))
    total_set = TotalSet.objects.get(game_id=game.game_id)
    total_set.set = []
    total_set.save()
    game.game_started = False
    game.new_game_requested = False
    game.my_bulls = None
    game.my_cows = None
    game.my_guess = None
    game.my_number = None
    game.your_bulls = None
    game.your_cows = None
    game.your_guess = None
    game.your_number = None
    game.attempts = 0
    game.available_digits_str = "0123456789"
    game.start_time = None
    game.finish_time = None
    game.upper_poster = upper_poster
    game.result_code = None
    game.save()


@login_required(login_url='login')
def fixture_list(request):
    fl_raw_data = FixtureList.objects.all()
    fl_data = get_data_for_fixture_table(fl_raw_data, User.objects.get)  ###
    return render(request, 'fixturelist.html', {'fl_data': fl_data})


def write_fl_to_db(request, game):
    start_timestamp = dt.datetime.timestamp(game.start_time)
    finish_timestamp = dt.datetime.timestamp(game.finish_time)
    f_list = FixtureList.objects.create(
        username=request.user,
        winner=game.result_code,
        attempts=game.attempts,
        time=game.start_time,
        duration=math.ceil((finish_timestamp - start_timestamp) / 60)
    )
    f_list.save()


def about(request):
    if request.method == 'POST':
        try:
            game = Game.objects.get(user=request.user)
        except Game.DoesNotExist:
            return JsonResponse({"my_number": None})
        return JsonResponse({"my_number": game.my_number})
    else:
        return render(request, "about.html")


@login_required(login_url='login')
def settings(request):
    if request.method == 'POST':
        form = SettingsForm(request.user, post_dict=request.POST)
        form.save()
        return JsonResponse({"success": True})
    else:
        form = SettingsForm(request.user)
    return render(request, "settings.html", {'form': form})

# проверить это. почему привилегии создаются в ткинтер-версии, а не здесь
# def create_user_privileges(request):
#     privileges = Privileges.objects.create(
#         username=request.user,
#         create_other=False,
#         modify_self = False,
#         modify_other = False,
#         delete_self = False,
#         delete_other = False
#     )
#     privileges.save()
