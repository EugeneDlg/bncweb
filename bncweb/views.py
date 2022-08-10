from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, HttpResponse
from .forms import SignUpForm
from django.http import JsonResponse
from django.template.context_processors import csrf
from crispy_forms.utils import render_crispy_form
from jsonview.decorators import json_view
from ..game.bnc_lib import read_config
from ..game.bnc_lib import validate_db_user

CONFIG_PATH = "bnc_config.yml"
settings = {}
settings = read_config(CONFIG_PATH)

import pdb


# from .models import Game


class MyAuthForm(AuthenticationForm):
    required_css_class = "myfield"
    nonfield_css_class = "myerror"


@json_view
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # user.first_name = form.cleaned_data['first_name']
            # user.last_name = form.cleaned_data["last_name"]
            # user.username = form.cleaned_data["username"]
            # user.password = form.cleaned_data["password1"]
            # user.email = form.cleaned_data["email"]
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data["password1"]
            signup_user = User.objects.get(username=username)
            # user_group = Group.objects.get(name='User')
            # user_group.user_set.add(signup_user)
            validate_db_user(username, "create", settings)  # for compatibility with Tkinter version
            create_db_user(username, password, settings)  # for compatibility with Tkinter version
            create_user_privileges(login, db_user)
            return {'success': True}
        ctx = {}
        ctx.update(csrf(request))
        form_html = render_crispy_form(form, context=ctx)
        print("ctx = {}")
        return {'success': False, 'form_html': form_html}

    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = MyAuthForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            # return render(request, 'home.html', {'capacity': request.game.capacity})
            else:
                return redirect('signup')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


# def validate_username(request):
#     username = request.GET.get('username', None)
#     response = {
#         'is_taken': User.objects.filter(username__iexact=username).exists()
#     }
#     return JsonResponse(response)


def signout_view(request):
    logout(request)
    return redirect('login')


def validate_game_data(request):
    # my_cows = request.GET.get('my_cows_', None)
    print("validate my cows")
    response = {
        'is_correct': False
    }
    return JsonResponse(response)


def test_ajax(request):
    if request.method == 'POST':
        flag = int(request.POST["flag"])
        print(flag)
        if not flag:

            print("testajax post flag false")
            login = request.POST["login"]
            password = request.POST["password"]

            if login == "1":
                response = {
                    'is_': False
                }
            else:
                response = {
                    'is_': True
                }
            return JsonResponse(response)
        print("testajax post flag true")
        return render(request, "testajax.html", {'aa': "QQQQQQQ"})
    print("testajax get")
    response = {
        'text': False
    }
    flag = request.POST.get("login", False)
    print("flag", flag)
    if flag:
        prefix = "QQQQQQ"
    else:
        prefix = "ZZZZZZ"
    return render(request, "testajax.html", {'aa': prefix})


def testpage(request):
    return render(request, "testpage.html")
