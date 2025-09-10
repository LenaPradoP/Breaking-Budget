from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

def login_user(request):
    # If already logged in, send to your main page
    if request.user.is_authenticated:
        return redirect("expenses:list_expenses")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("expenses:list_expenses")
    else:
        form = AuthenticationForm(request)

    return render(request, "users/login.html", {"form": form})

@login_required
def logout_user(request):
    if request.method == "POST":
        logout(request)
        return redirect("users:login")
    return redirect("expenses:list_expenses")

def home(request):
    return redirect("expenses:list_expenses")
