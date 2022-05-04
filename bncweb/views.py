from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from .forms import SignUpForm
from .models import Game


class MyAuthForm(AuthenticationForm):
	required_css_class = "myfield"
	nonfield_css_class = "myerror"


def signup_view(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			signup_user = User.objects.get(username=username)
			# user_group = Group.objects.get(name='User')
			# user_group.user_set.add(signup_user)
	else:
		form = SignUpForm()
	return render(request, 'signup.html', {'form': form})


def login_view(request):
	fl = False
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
			fl = True
	else:
		form = AuthenticationForm()
	if fl:
		return render(request, 'login.html', {'form': form})
	return render(request, 'login.html', {'form': form})

# def validate_username(request):
#     username = request.GET.get('username', None)
#     response = {
#         'is_taken': User.objects.filter(username__iexact=username).exists()
#     }
#     return JsonResponse(response)


@login_required(login_url='login')
def home(request):
	if request.method == "POST":
		print("POST")
	else:
		print("GET")
		game = Game.objects.get(game_id=request.session.session_key)
	return render(request, 'home.html')
	# return render(request, 'home.html', )


def signout_view(request):
	logout(request)
	return redirect('login')