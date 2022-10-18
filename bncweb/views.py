from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.template.context_processors import csrf

from crispy_forms.utils import render_crispy_form
from jsonview.decorators import json_view

from .bnc_lib import read_config, validate_db_user, create_db_user, modify_db_user, send_email
from .forms import SignUpForm
from game.models import Game


CONFIG_PATH = "bnc_config.yml"
settings = read_config(CONFIG_PATH)


class MyAuthForm(AuthenticationForm):
    required_css_class = "myfield"
    nonfield_css_class = "myerror"


@json_view
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        # form_ext = SignUpFormExt(request.POST, request.FILES)
        breakpoint()
        if form.is_valid():
            # user.first_name = form.cleaned_data['first_name']
            # user.last_name = form.cleaned_data["last_name"]
            # user.username = form.cleaned_data["username"]
            # user.password = form.cleaned_data["password1"]
            # user.email = form.cleaned_data["email"]
            form.save()
            username = form.cleaned_data["username"]
            firstname = form.cleaned_data["first_name"]
            lastname = form.cleaned_data["last_name"]
            password = form.cleaned_data["password1"]
            email = form.cleaned_data["email"]
            # form_ext.save()
            # avatar = form_ext.cleaned_data["avatar"]
            # signup_user = User.objects.get(username=username)
            # user_group = Group.objects.get(name='User')
            # user_group.user_set.add(signup_user)
            validate_db_user(settings, username, "create")  # for compatibility with GUI Tkinter version
            # create_db_user(settings, username, password)  # for compatibility with GUI Tkinter version
            replace_list = (("FIRSTNAME", firstname), ("LASTNAME", lastname))
            # try:
            # send_email(settings, email, "welcome", replace_list)
            # except Exception as exc:
            #     raise exc
            return {'success': True}
        breakpoint()
        ctx = {}
        ctx.update(csrf(request))
        form_html = render_crispy_form(form, context=ctx)
        return {'success': False, 'form_html': form_html}
    else:
        form = SignUpForm()
        # form_ext = SignUpFormExt()
        # breakpoint()
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
    try:
        game = Game.objects.get(game_id=request.session.session_key)
        game.delete()
    except Exception:
        raise
    logout(request)
    return redirect('login')


# def validate_game_data(request):
#     # my_cows = request.GET.get('my_cows_', None)
#     print("validate my cows")
#     response = {
#         'is_correct': False
#     }
#     return JsonResponse(response)


class MyPasswordResetConfirmView(PasswordResetConfirmView):
    def form_valid(self, form):
        # breakpoint()
        user = form.save()
        password = form.cleaned_data["new_password1"]
        # for compatibility with GUI Tkinter version
        modify_db_user(settings, str(user), password)
        return super().form_valid(form)