from dataclasses import fields
from turtle import textinput
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UserLog
from .models import Space
from django import forms
from .models import Group

from django.forms.widgets import PasswordInput, TextInput


class CreateUserForm(UserCreationForm):
    
    class Meta:
        
        model = User
        fields = ['username','email','password1','password2']
        


class LoginForm(AuthenticationForm):
    
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())
    
class UserLogForm(forms.ModelForm):
    
    class Meta:
        model = UserLog
        fields = ['title','information']

class CreateSpaceForm(forms.ModelForm):
    class Meta:
        model = Space
        fields = ['name']
       
class SpaceCodeForm(forms.Form):
    code = forms.CharField(label="Enter Code", max_length=8)

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'members']        