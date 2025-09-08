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
        update_session_auth_hash(request, form.user)
        return redirect('users:password_changed', pk=user.pk) #Just to try update_user works. Delete after User Detail is implemented. 
    else:
        return render(request, 'users/edit_user.html', context)

#Just to try update_user works. Delete after User Detail is implemented. 
def password_changed_success(request, pk):
    return HttpResponse(f"Password changed successfully for user {pk}!")