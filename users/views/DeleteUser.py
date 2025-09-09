
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from ..models import CustomUser
from django.contrib import messages


@login_required
def delete_user(request, pk):
    user_to_delete = get_object_or_404( CustomUser, pk=pk)
    if request.user.is_superuser:
        user_to_delete.delete()
        messages.success(f"User {user_to_delete} has been deleted")
        return redirect('users:view_users')
    if request.user.role.lower() != "admin":
        messages.error(request, "Only admins can delete users.")
        return redirect('users:view_users')
    if user_to_delete == request.user or user_to_delete.role.lower() == "admin":
        messages.error(request, "Admins cannot delete themselves or other admins.")
        return redirect('users:view_users')
    user_to_delete.delete()
    messages.success(request, f"Traveler {user_to_delete} has been deleted.")
    return redirect('users:view_users')