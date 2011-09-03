from django.db import models
from django import forms
from django.contrib.auth.models import User
import datetime

# Create your models here.
    
class SignupForm(forms.Form):
    username = forms.CharField(max_length=30)
    email = forms.EmailField()
    password1 = forms.CharField(max_length=30,
                                widget=forms.PasswordInput())
    password2 = forms.CharField(max_length=30,
                                widget=forms.PasswordInput())
    def clean_username(self):
        try:
            User.objects.get(username=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError("This username is already in use.Please choose another.")
    
    def clean_password2(self):
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            raise forms.ValidationError("You must type the same password each time")
        return self.cleaned_data['password2']

    

    def save(self):
        new_user = User.objects.create_user(username=self.cleaned_data['username'],
                                            email=self.cleaned_data['email'],
                                            password=self.cleaned_data['password1'])
        return new_user

class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30,
                               widget=forms.PasswordInput())
