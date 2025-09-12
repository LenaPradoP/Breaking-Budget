from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from users.forms import AdminUserEditForm
from ..models import CustomUser


"""
edit_user:
Handles user editing based on permissions:
    - Any user (traveler/admin) editing their own account: can only change password
    - Admin editing another user's account: can edit profile info (username, email, etc.) but NOT password or role
    - Travelers cannot edit other users' accounts (forbidden)

update_user:
Processes form submission for user editing with same permission logic as edit_user:
    - User editing own account: validates and saves password change, preserves login session
    - Admin editing other user: validates and saves profile data changes
    - Travelers editing other accounts: forbidden (403 error)
Returns to user detail on success, or back to edit form with validation errors
"""

@login_required
def edit_user(request, pk):
    user_to_edit = get_object_or_404(CustomUser, pk=pk, is_superuser=False)
    
    if request.user.pk == user_to_edit.pk:
        form = PasswordChangeForm(user=request.user)
    elif request.user.role == CustomUser.Role.ADMIN:
        if user_to_edit.role == CustomUser.Role.ADMIN or user_to_edit.is_superuser:
            raise PermissionDenied("Admins cannot edit other admins or superusers.")
        form = AdminUserEditForm(instance=user_to_edit)
    
    context = {
        'form': form,
        'user': user_to_edit
    }
    
    return render(request, 'users/edit_user.html', context)

@login_required
def update_user(request, pk):

    if request.method != "POST":
        return redirect("users:edit_user", pk=pk)

    user_to_update = get_object_or_404(CustomUser, pk=pk, is_superuser=False)
    
    if request.user.pk == user_to_update.pk:
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)
            return redirect("users:user_detail", pk=user_to_update.pk)
        context = {
            'form': form,
            'user': user_to_update
        }
        return render(request, "users/edit_user.html", context)
    
    if request.user.role == CustomUser.Role.ADMIN:
        if user_to_update.role == CustomUser.Role.ADMIN or user_to_update.is_superuser:
            raise PermissionDenied("Admins cannot edit other admins or superusers.")
        form = AdminUserEditForm(instance=user_to_update, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("users:user_detail", pk=user_to_update.pk)
        context = {
            'form': form,
            'user': user_to_update
        }
        return render(request, "users/edit_user.html", context)
    
    raise PermissionDenied("You don't have permission to edit this user.")
