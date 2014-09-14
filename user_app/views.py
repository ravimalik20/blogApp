from django.shortcuts import render, HttpResponseRedirect
from user_app.forms import SignupForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

def signin(request, redirect_to = ""):
	form = LoginForm()
	template = "user_app/templates/login.html"
	errors = []	
	if request.method == "POST":
		form = LoginForm(request.POST)
		if form.is_valid():
			usr = form.cleaned_data["username"]
			pwd = form.cleaned_data["password"]

			user = authenticate(username = usr, password = pwd)
			if not user :
				errors.append("Invalid username password.")
			elif user.is_active:
				login(request, user)
				return HttpResponseRedirect(redirect_to)
			else:
				errors.append("User not active. Contact System Admin.")
		else:
			errors.append("Invalid username password.")
	
	return render(request, template, {'form':form, 'errors':errors})

def signout(request, redirect_to = "/user/login/"):
	logout(request)
	return HttpResponseRedirect(redirect_to)

def signup(request, redirect_to = "/user/login/"):
	form = SignupForm()
	template = "user_app/templates/signup.html"
	errors = []
	if request.method == "POST":
		form = SignupForm(request.POST)
		if form.is_valid():
			usr = form.cleaned_data["username"]
			pwd1 = form.cleaned_data["pwd1"]
			pwd2 = form.cleaned_data["pwd2"]
			email = form.cleaned_data["email"]
			if pwd1 == pwd2:
				user = User.objects.create_user(usr, email, pwd1)
				user.save()
				return HttpResponseRedirect(redirect_to)
			else:
				errors.append("Passwords donot match.")
		else:
			errors.append("Invalid Form Data.")

	return render(request, template, {'errors':errors, 'form':form})

