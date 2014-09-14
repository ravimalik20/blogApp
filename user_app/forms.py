from django import forms
from django.contrib.auth.models import User

class SignupForm(forms.Form):
	username = forms.CharField(max_length=32)
	pwd1 = forms.CharField( max_length=32, widget=forms.PasswordInput)
	pwd2 = forms.CharField( max_length=32, widget=forms.PasswordInput)
	email = forms.EmailField()

class LoginForm(forms.Form):
	username = forms.CharField(max_length=32)
	password = forms.CharField(max_length=32, widget=forms.PasswordInput)
