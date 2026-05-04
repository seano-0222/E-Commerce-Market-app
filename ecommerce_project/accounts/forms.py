from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


# REGISTER FORM
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# EDIT PROFILE FORM
class EditProfileForm(UserChangeForm):
    password = None  # hide password field

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']