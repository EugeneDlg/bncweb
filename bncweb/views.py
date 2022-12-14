import re

from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from .models import Visitors


def login_view(request):
    if request.method == 'POST':
        # form = MyAuthForm(data=request.POST)
        form = AuthenticationForm(data=request.POST)
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
            response = render(request, 'login.html', {'form': form})
            response.status_code = 401
            return response
    else:
        ip_address = get_ip_address(request)
        client_info = request.META['HTTP_USER_AGENT']
        match = re.search(r'.* \((.*)\)\s+(.*)', client_info)
        client_os = match.group(1).strip()
        client_browser = match.group(2).strip()
        visitor = Visitors.objects.create(
            ip_address=ip_address,
            os=client_os,
            browser=client_browser,
            time=timezone.now(),
        )
        if request.user.is_authenticated:
            return redirect('home')
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def get_ip_address(request):
    client_ip = request.META.get("HTTP_X_FORWARDED_FOR")
    if client_ip:
        ip_address = client_ip.split(',')[-1]
    else:
        ip_address = request.META.get("REMOTE_ADDR")
    return ip_address


# # for compatibility with GUI Tkinter version
# class MyPasswordResetConfirmView(PasswordResetConfirmView):
#     def form_valid(self, form):
#         user = form.save()
#         password = form.cleaned_data["new_password1"]
#         modify_db_user(settings, str(user), password)
#         return super().form_valid(form)
#
#