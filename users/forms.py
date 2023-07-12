from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from users.models import User


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class UserProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('email', 'phone', 'avatar', 'country')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].wiget = forms.HiddenInput
