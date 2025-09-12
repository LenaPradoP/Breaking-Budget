from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages

from ..forms import CustomUserWebCreateForm
from ..models import CustomUser


# Helper function to check if user is admin
def _ensure_admin(request):
    # Allow admins only
    if not request.user.role == CustomUser.Role.ADMIN:
        raise PermissionDenied("Only admins can create users.")


@login_required
def new_user(request):
    _ensure_admin(request)
    form = CustomUserWebCreateForm()
    return render(request, "users/new.html", {"form": form})

@login_required
def create_user(request):
    if request.method != "POST":
        return redirect("users:new_user")
    _ensure_admin(request)
    form = CustomUserWebCreateForm(request.POST)
    if form.is_valid():
        user = form.save(commit=False)          # no form.save override
        user.role = CustomUser.Role.TRAVELER    # force traveler role
        user.save()
        messages.success(request, f"Traveler {user.username} was created.")
        return redirect("users:view_users")
    return render(request, "users/new.html", {"form": form})
