from pyexpat import model
from urllib.parse import uses_relative
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django import forms
class CustomerUserForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2']


        