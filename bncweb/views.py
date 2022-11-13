from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User


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
        if request.user.is_authenticated:
            return redirect('home')
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


# # for compatibility with GUI Tkinter version
# class MyPasswordResetConfirmView(PasswordResetConfirmView):
#     def form_valid(self, form):
#         user = form.save()
#         password = form.cleaned_data["new_password1"]
#         modify_db_user(settings, str(user), password)
#         return super().form_valid(form)
#
#