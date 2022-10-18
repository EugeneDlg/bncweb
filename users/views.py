from django.shortcuts import render
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

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
        # breakpoint()
        return {"success": False, "form_html": form_html}
    else:
        # breakpoint()
        form = PasswordChangeForm(request.user)
    return render(request, "edit.html", {"form": form, "url_type":"changepassword", "label":"Change your password"})


@login_required(login_url='login')
@json_view
def edit_profile(request):
    if request.method == "POST":
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return {"success": True}
        context = csrf(request)
        form_html = render_crispy_form(form, context=context)
        return {"success": False, "form_html": form_html}
    else:
        # breakpoint()
        form = UserEditForm(instance=request.user)
    return render(request, "edit.html", {"form": form, "url_type":"edit", "label":"Edit your profile"})


@login_required(login_url='login')
@json_view
def delete_profile(request):
    pass
    # if request.method == "POST":
    #     form = UserEditForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return {"success": True}
    #     context = csrf(request)
    #     form_html = render_crispy_form(form, context=context)
    #     return {"success": False, "form_html": form_html}
    # else:
    #     breakpoint()
    #     form = UserEditForm(instance=request.user)
    # return render(request, "usermanage.html", {"form": form})