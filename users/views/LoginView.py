from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django import forms

# Simple form for manual login
class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

def login_user(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                return redirect("users:home") 
            form.add_error(None, "Invalid username or password")
    else:
        form = LoginForm()
    return render(request, "users/login.html", {"form": form})

def home(request):
    return render(request, "users/home.html")
