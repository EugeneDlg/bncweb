from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .bnc_tk import Game
import os


def loginView(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        # if form.is_valid():
        username = request.POST['username']
        password = request.POST['password']
        # user = authenticate(username=username, password=password)
        user = Game.authenticate_user(username, password)
        if user is not None:
            # login(request, user)
            return redirect("home")
        else:
            return redirect("signup")
    else:
        form = AuthenticationForm()
    return render(request, "login2.html", {"form": form})


def home(request):
    f = os.getcwd()
    return render(request, "home.html", {"cwg": f})


def signup(request):
    return render(request, "signup.html")


def verify_username(request):
    username = request.GET.get('username', None)
    response = {"exists": True}
    return JsonResponse(response)


def login(request):
    return render(request, "login1.html")
    # return redirect("home")

