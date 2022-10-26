import datetime as dt
import math
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from jsonview.decorators import json_view
from crispy_forms.utils import render_crispy_form

from .models import Game, MyHistory, YourHistory, TotalSet, FixtureList
from .forms import SettingsForm

from .bnc_lib import get_my_first_guess, think_of_number_for_you, make_my_guess, validate_cows_and_bulls
from .bnc_lib import BnCException, validate_your_guess, make_your_guess, FinishedNotOKException
from .bnc_lib import get_data_for_fixture_table, read_config


CONFIG_PATH = "bnc_config.yml"
initial_settings = read_config(CONFIG_PATH)


@login_required(login_url='login')
def home(request):
    if request.method == "POST":
        print("home_post")
        # game = Game.objects.get(game_id=request.session.session_key)
        game = Game.objects.get(user=request.user)
    else:
        print("home_get")
        try:
            # game = Game.objects.get(game_id=request.session.session_key)
            game = Game.objects.get(user=request.user)
            game.upper_poster = "Please think of a number with " + str(game.capacity) + " digits"
            game.save()
        except Game.DoesNotExist:
            print("game object created initially")

            game = Game.objects.create(
                game_id=request.session.session_key,
                upper_poster="Please think of a number with " + str(initial_settings["default_capacity"]) + " digits",
                capacity=initial_settings["default_capacity"],
                user=request.user
            )
            my_history = MyHistory.objects.create(
                game_id=game
            )
            your_history = YourHistory.objects.create(
                game_id=game
            )
            total_set = TotalSet.objects.create(
                game_id=game
            )
        if game.attempts > 0:
            if game.dual_game:
                return redirect('dualgame')
            else:
                return redirect('singlegame')
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
            print("attempts=0")
            # if not submit_flag:
            #     return JsonResponse({"is_OK": True})
            game.my_guess = get_my_first_guess(game.capacity)
            game.my_number = think_of_number_for_you(game.capacity)
            game.attempts += 1
            game.start_time = timezone.now()
            game.game_started = True
            game.new_game_requested = False
            game.upper_poster = "I wish you an interesting game!:-)"
            game.result_code = None
            game.save()
            return render(request, 'dualgame.html', {'game': game})
        else:
            if game.new_game_requested:
                breakpoint()
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
                if game.dual_game:
                    your_guess_entered = request.POST["your_guess"]
                try:
                    validate_cows_and_bulls(my_cows_entered, my_bulls_entered, game.capacity)
                    validate_your_guess(game.capacity, your_guess_entered)
                except BnCException as exc:
                    response = {"success": False, "items": exc.msg}
                    return JsonResponse(response)
                except Exception as exc:
                    raise exc
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
            if my_result and not your_result:
                game.result_code = 1
            if your_result and not my_result:
                game.result_code = 2
            if your_result and my_result:
                game.result_code = 3
            game.save()
            if game.result_code is not None:
                finish_dual_game(request, game)
            return render(request, 'dualgame.html', {'game': game,
                                                     'my_items': my_history.items, 'your_items': your_history.items})
    else:
        print("GET dualgame")
        # create_user_privileges(request)
        try:
            game = Game.objects.get(user=request.user)
            my_history = MyHistory.objects.get(game_id=game.game_id)
            your_history = YourHistory.objects.get(game_id=game.game_id)
        except Game.DoesNotExist:
            game = Game.objects.create(
                game_id=request.session.session_key,
                game_started=False,
                upper_poster="Please think of a number with " + str(initial_settings["default_capacity"]) + " digits",
                capacity=initial_settings["default_capacity"],
                attempts=0
            )
        if game.attempts == 0:
            return redirect('home')
    return render(request, 'dualgame.html', {'game': game,
                                             'my_items': my_history.items, 'your_items': your_history.items})


@login_required(login_url='login')
def single_game(request):
    return render(request, 'singlegame.html')


@login_required(login_url='login')
def users_view(request):
    return render(request, 'users.html')


def finish_dual_game(request, game):
    result_code = game.result_code
    game.finish_time = timezone.now()
    if result_code > 0:
        write_fl_to_db(request, game)
    game.game_started = False
    game.new_game_requested = True
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
    game.save()


def reset_to_initials(game):
    my_history = MyHistory.objects.get(game_id=game.game_id)
    my_history.items = []
    my_history.save()
    your_history = YourHistory.objects.get(game_id=game.game_id)
    your_history.items = []
    your_history.save()
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
    game.upper_poster = "Please think of a number with " + str(game.capacity) + " digits"
    game.result_code = None
    game.save()


# def new_game(request):
#     game = Game.objects.get(user=request.user)
#     if not game.game_started:
#         return redirect('home')
#     my_history = MyHistory.objects.get(game_id=request.session.session_key)
#     your_history = YourHistory.objects.get(game_id=request.session.session_key)
#     total_set = TotalSet.objects.get(game_id=request.session.session_key)
#     game.delete()
#
#     game = Game.objects.create(
#         game_id=request.session.session_key,
#         game_started=False,
#         upper_poster="Please think of a number with " + initial_settings["default_capacity"] + " digits",
#         capacity=initial_settings["default_capacity"],
#         attempts=0
#     )
#     my_history = MyHistory.objects.create(
#         game_id=game
#     )
#     your_history = YourHistory.objects.create(
#         game_id=game
#     )
#     total_set = TotalSet.objects.create(
#         game_id=game
#     )
#     # my_history.items = []
#     # my_history.save()
#     # your_history.items = []
#     # your_history.save()
#     # total_set.set = []
#     # total_set.save()
#     # game.game_started = False
#     # game.my_bulls = None
#     # game.my_cows = None
#     # game.my_guess = None
#     # game.my_number = None
#     # game.your_bulls = None
#     # game.your_cows = None
#     # game.your_guess = None
#     # game.your_number = None
#     # game.capacity = 4
#     # game.attempts = 0
#     # game.available_digits_str = "0123456789"
#     # game.start_time = None
#     # game.finish_time = None
#     # game.dual_game keeps the previous state
#     game.new_game_requested = True
#     game.save()
#     return redirect('home')


def fixture_list(request):
    # print("User: ", User.objects.get(username='greta0').first_name)
    fl_raw_data = FixtureList.objects.all()
    fl_data = get_data_for_fixture_table(fl_raw_data, User.objects.get) ###
    return render(request, 'fixturelist.html', {'fl_data': fl_data})
    # return render(request, 'singlegame.html')


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
    return render(request, "about.html")


def settings(request):
    if request.method == 'POST':
        form = SettingsForm(request.user, post_dict=request.POST)
        form.save()
        return redirect('home')
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


# @login_required(login_url='login')
# @json_view
# def edit_profile(request):
#     if request.method == "POST":
#         form = UserEditForm(request.POST, instance=request.user)
#         if form.is_valid():
#             form.save()
#             return {"success": True}
#         context = csrf(request)
#         form_html = render_crispy_form(form, context=context)
#         return {"success": False, "form_html": form_html}
#     else:
#         # breakpoint()
#         form = UserEditForm(instance=request.user)
#     return render(request, "edit.html", {"form": form, "url_type":"edit", "label":"Edit your profile"})


# @login_required(login_url='login')
# @json_view
# def delete_profile(request):
#     pass
#     # if request.method == "POST":
#     #     form = UserEditForm(request.POST)
#     #     if form.is_valid():
#     #         form.save()
#     #         return {"success": True}
#     #     context = csrf(request)
#     #     form_html = render_crispy_form(form, context=context)
#     #     return {"success": False, "form_html": form_html}
#     # else:
#     #     breakpoint()
#     #     form = UserEditForm(instance=request.user)
#     # return render(request, "usermanage.html", {"form": form})


# @login_required(login_url='login')
# @json_view
# def changepassword(request):
#     if request.method == "POST":
#         form = PasswordChangeForm(request.user, request.POST)
#         if form.is_valid():
#             user = form.save()
#             update_session_auth_hash(request, user)
#             return {"success": True}
#         context = csrf(request)
#         form_html = render_crispy_form(form, context=context)
#         # breakpoint()
#         return {"success": False, "form_html": form_html}
#     else:
#         # breakpoint()
#         form = PasswordChangeForm(request.user)
#     return render(request, "edit.html", {"form": form, "url_type":"changepassword", "label":"Change your password"})





