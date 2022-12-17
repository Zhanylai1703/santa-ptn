from django import forms
# from django.contrib.auth.models import User
from .models import Owner
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = Owner
        fields = ['username', 'email', 'password1', 'password2']