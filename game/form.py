from django import forms
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User


class UserEditForm(UserChangeForm):
    # def __init__(self, *args, **kwargs):
        # super().__init__(*args, **kwargs)
        # self.fields['password'].
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(max_length=250, required=True, help_text='eg. youremail@gmail.com')
    password = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')



