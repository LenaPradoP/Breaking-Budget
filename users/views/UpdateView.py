from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
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

def edit_user(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    
    if request.user.pk == pk:
        form = PasswordChangeForm(user=user)
    elif request.user.role == 'admin':
        form = AdminUserEditForm(instance=user)
    else:
        raise PermissionDenied("You don't have permission to edit this user")
    
    context = {
        'form': form,
        'user': user
    }
    
    return render(request, 'users/edit_user.html', context)

def update_user(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    
    if request.user.pk == pk:
        form = PasswordChangeForm(user=user, data=request.POST)
    elif request.user.role == 'admin':
        form = AdminUserEditForm(instance=user, data=request.POST)
    else:
        raise PermissionDenied("You don't have permission to edit this user")
    
    context = {
        'form': form,
        'user': user
    }

    if form.is_valid():
        form.save()
        
        if request.user.pk == pk:
            update_session_auth_hash(request, form.user)
        
        return redirect('users:user_detail', pk=user.pk)
    else:
        return render(request, 'users/edit_user.html', {
            'form': form,
            'user': user
        })