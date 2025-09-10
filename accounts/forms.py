from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser

class RegisterUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["email", "name", "password1", "password2"]
