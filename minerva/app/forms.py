from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput

from .models import *


class CustomUserCreationForm(UserCreationForm):
    
    class Meta:
        model=User
        fields=['username','email','password1','password2']

#login user
class LoginForm(AuthenticationForm):
    username=forms.CharField(widget=TextInput())
    password=forms.CharField(widget=PasswordInput())

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = '__all__'

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'

class periodicoForm(forms.ModelForm):
    class Meta:
        model=Periodico
        fields = '__all__'