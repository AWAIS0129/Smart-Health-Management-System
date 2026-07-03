from . import models
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = models.User
        fields = [
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
            'country',
            'city',
            'date_of_birth',
            'gender',
            'mobile_number',
        ]

class  UserLoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email')