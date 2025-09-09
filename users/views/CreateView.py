from django.shortcuts import render
from django import forms
from ..forms import CustomUserWebCreateForm
from django.contrib.auth.decorators import login_required

@login_required
def new_user(request):
    form = CustomUserWebCreateForm()
    return render(request, "users/new.html", {"form": form})

@login_required
def create_user(request):
    if request.method != "POST":
        form = CustomUserWebCreateForm()
        return render(request, "users/new.html", {"form": form})
    form = CustomUserWebCreateForm(request.POST)
    if form.is_valid():
        user = form.save()
        return render(request, "users/create.html", {"user": user})
    return render(request, "users/new.html", {"form": form})  
