from django.shortcuts import render
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.shortcuts import render, redirect

from crispy_forms.utils import render_crispy_form
from jsonview.decorators import json_view
from django.template.context_processors import csrf

from .bnc_lib import read_config, validate_db_user, create_db_user, modify_db_user, send_email
from .forms import SignUpForm, UserEditForm

CONFIG_PATH = "bnc_config.yml"
settings = read_config(CONFIG_PATH)


@json_view
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            firstname = form.cleaned_data["first_name"]
            lastname = form.cleaned_data["last_name"]
            password = form.cleaned_data["password1"]
            email = form.cleaned_data["email"]
            # signup_user = User.objects.get(username=username)
            # user_group = Group.objects.get(name='User')
            # user_group.user_set.add(signup_user)
            validate_db_user(settings, username, "create")  # for compatibility with GUI Tkinter version
            create_db_user(settings, username, password)  # for compatibility with GUI Tkinter version
            replace_list = (("FIRSTNAME", firstname), ("LASTNAME", lastname))
            try:
                send_email(settings, email, "welcome", replace_list)
            except Exception as exc:
                raise exc
            return {'success': True}
        ctx = {}
        ctx.update(csrf(request))
        form_html = render_crispy_form(form, context=ctx)
        return {'success': False, 'form_html': form_html}
    else:
        if request.user.is_authenticated:
            return redirect('edit')
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


@login_required(login_url='login')
def signout_view(request):
    game = request.user.game
    game.delete()
    logout(request)
    return redirect('login')


class MyPasswordResetConfirmView(PasswordResetConfirmView):
    def form_valid(self, form):
        user = form.save()
        password = form.cleaned_data["new_password1"]
        # for compatibility with GUI Tkinter version
        modify_db_user(settings, str(user), password)
        return super().form_valid(form)


@login_required(login_url='login')
@json_view
def changepassword(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return {"success": True}
        context = csrf(request)
        form_html = render_crispy_form(form, context=context)
        return {"success": False, "form_html": form_html}
    else:
        # breakpoint()
        form = PasswordChangeForm(request.user)
    return render(request, "edit.html", {"form": form, "url_type":"changepassword", "label":"Change your password"})


@login_required(login_url='login')
@json_view
def edit_profile(request):
    if request.method == "POST":
        form = UserEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return {"success": True}
        context = csrf(request)
        form_html = render_crispy_form(form, context=context)
        return {"success": False, "form_html": form_html}
    else:
        # breakpoint()
        form = UserEditForm(instance=request.user)
    return render(request, "edit.html", {"form": form, "url_type": "edit", "label": "Edit your profile"})


@login_required(login_url='login')
def delete_profile(request):
    if request.method == "POST":
        user = User.objects.get(username=request.user)
        user.delete()
        logout(request)
        return redirect('login')
    else:
        return render(request, "delete.html")