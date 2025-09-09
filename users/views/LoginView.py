from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django import forms
from django.contrib.auth.forms import AuthenticationForm

def login_user(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("users:home")
    else:
        form = AuthenticationForm(request)
    return render(request, "users/login.html", {"form": form})


def home(request):
    return render(request, "users/home.html")
