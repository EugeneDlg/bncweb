from django.shortcuts import render
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.core.mail import send_mail
from django.conf import settings

from crispy_forms.utils import render_crispy_form
from jsonview.decorators import json_view

from bncutils.bnc_lib import read_config, validate_db_user, create_db_user, modify_db_user, send_email
from .forms import SignUpForm, UserEditForm


initial_settings = read_config()


@json_view
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        context = csrf(request)
        form_html = render_crispy_form(form, context=context)
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
            validate_db_user(initial_settings, username, "create")  # for compatibility with GUI Tkinter version
            create_db_user(initial_settings, username, password)  # for compatibility with GUI Tkinter version
            replace_list = (("FIRSTNAME", firstname), ("LASTNAME", lastname))
            try:
                send_email(initial_settings, email, "welcome", replace_list)
            except Exception as exc:
                raise exc
            return {"success": True, "form_html": form_html}
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
        modify_db_user(initial_settings, str(user), password)
        return super().form_valid(form)


@login_required(login_url='login')
@json_view
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        context = csrf(request)
        form_html = render_crispy_form(form, context=context)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            subject = "Your password has been changed"
            html_message = "You received this message because you or someone else " \
                           "has recently changed your password in <b>BnC game</b>.<br>" \
                           "Please be aware of that. <br><br>" \
                           "<b>Best regards, BnC team</b>"
            message = "You received this message because you or someone else " \
                      "has recently changed your password in BnC game." \
                      "Please be aware of that." \
                      "Best regards, BnC team"
            from_email = settings.EMAIL_HOST_USER
            to_email = user.email
            send_mail(subject, message, from_email, [to_email], html_message=html_message)
            return {"success": True, "form_html": form_html}
        return {"success": False, "form_html": form_html}
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "edit.html", {"form": form, "url_type": "change_password", "label": "Change your password"})


@login_required(login_url='login')
@json_view
def edit_profile(request):
    if request.method == "POST":
        if request.POST.get("delete_av", False):
            request.user.delete_avatar()
            return {"success": True}
        form = UserEditForm(request.POST, request.FILES, instance=request.user)
        context = csrf(request)
        form_html = render_crispy_form(form, context=context)
        if form.is_valid():
            form.save()
            return {"success": True, "form_html": form_html}
        return {"success": False, "form_html": form_html}
    else:
        form = UserEditForm(instance=request.user)
    return render(request, "edit.html", {"form": form, "url_type": "edit",
                                         "label": "Edit your profile",
                                         "default_avatar": "/media/images/your_default_av.png",
                                         "is_admin": request.user == initial_settings["admin_user"]})


@login_required(login_url='login')
def delete_profile(request):
    if request.method == "POST":
        user = User.objects.get(username=request.user)
        user.delete()
        logout(request)
        return redirect('login')
    else:
        return render(request, "delete.html")
