from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import User
from .models import Extension


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(max_length=250, required=True, help_text='eg. youremail@gmail.com')
    avatar = forms.ImageField(max_length=950, required=False,
                              help_text="Max. volume is 1 Mb. Max. height and width are 600px")

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2', 'email', 'avatar')

    def save(self):
        user = super().save()
        # user has to be saved to add profile
        # user.save()
        # ext = Extension.objects.create(user=self)
        # ext.avatar = self.cleaned_data.get('avatar')
        # ext.save()
        user.create_extension()
        user.extension.avatar = self.cleaned_data.get('avatar')
        user.extension.save()


class UserEditForm(UserChangeForm):

    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(max_length=250, required=True, help_text='eg. youremail@gmail.com')
    # password = forms.CharField(widget=forms.HiddenInput())
    avatar = forms.ImageField(max_length=950, required=False,
                              help_text="Max. volume is 1 Mb. Max. height and width are 600px")

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'avatar')

    def save(self):
        user = super().save()
        avatar = self.cleaned_data.get('avatar')
        if avatar is not None:
            user.extension.avatar = avatar
            user.extension.save()
