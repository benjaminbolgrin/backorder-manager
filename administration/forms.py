from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User, Group
from django.db import models
import random
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class UserCreateForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'groups']


class UserPasswordForm(forms.Form):

    password1 = forms.CharField(widget=forms.PasswordInput, label='New Password')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if not password2:
            raise forms.ValidationError("Please confirm the password")

        if password1 != password2:
            raise forms.ValidationError("The passwords don't match")

        return password2
