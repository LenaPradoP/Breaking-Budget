from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django import forms
from ..forms import CustomUserWebCreateForm
from ..models import CustomUser

def new_user(request):
    form = CustomUserWebCreateForm()
    return render(request, "users/new.html", {"form": form})

def create_user(request):
    if request.method != "POST":
        form = CustomUserWebCreateForm()
        return render(request, "users/new.html", {"form": form})
    form = CustomUserWebCreateForm(request.POST)
    if form.is_valid():
        user = form.save()
        return render(request, "users/create.html", {"user": user})
    return render(request, "users/new.html", {"form": form})  
