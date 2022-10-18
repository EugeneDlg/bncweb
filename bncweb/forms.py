from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


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
        # user.first_name = self.cleaned_data['first_name']
        # user.last_name = self.cleaned_data['last_name']
        # user.email = self.cleaned_data['email']

        # user has to be saved to add profile
        # user.save()
        breakpoint()
        user.create_user_ext()
        user.userext.avatar = self.cleaned_data.get('avatar')
        user.userext.save()
        # user.save()


# class SignUpFormExt(forms.ModelForm):
#     avatar = forms.ImageField(max_length=950, required=False,
#                               help_text="Max. volume is 1 Mb. Max. height and width are 600px")
#     middle_name = forms.CharField(max_length=100, required=True)
#
#     class Meta:
#         model = UserExt
#         fields = ('avatar', 'middle_name')