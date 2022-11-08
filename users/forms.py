import re

from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import User
from bncutils.bnc_lib import read_config


initial_settings = read_config()


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(max_length=250, required=True, help_text='eg. youremail@gmail.com')
    avatar = forms.ImageField(max_length=950, required=False,
                              help_text="Max. volume is 2 Mb. Valid formats are jpeg, png, gif.")

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2', 'email', 'avatar')

    def save(self):
        user = super().save()
        user.create_extension()
        user.extension.avatar = self.cleaned_data.get('avatar')
        user.extension.save()


class UserEditForm(UserChangeForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(max_length=250, required=True, help_text='eg. youremail@gmail.com')
    # password = forms.CharField(widget=forms.HiddenInput())
    avatar = forms.ImageField(max_length=950, required=False,
                              help_text="Max. volume is 2 Mb. Valid formats are jpeg, png, gif.")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs["instance"]
        if str(instance) == initial_settings["admin_user"]:
            self.fields["username"].disabled = True

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'avatar')

    def save(self):
        user = super().save()
        avatar = self.cleaned_data.get('avatar')
        if avatar is not None:
            user.extension.avatar = avatar
            user.extension.save()

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar is None:
            return None
        s = re.search(r".*\.(?:jpeg|jpg|gif|png)$", avatar.name, re.IGNORECASE)
        if s is None:
            raise forms.ValidationError("Invalid file format. Supported format: jpeg, png, gif...")
        if avatar.size > 2*1024*1024:
            raise forms.ValidationError("File size cannot be greater than 2Mb...")
        return avatar
