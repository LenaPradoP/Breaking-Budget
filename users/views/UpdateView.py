from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from users.forms import CustomUserChangeForm
from ..models import CustomUser

def edit_user(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)

    if request.user.role == 'admin':
        form = CustomUserChangeForm(user=user)
    else:
        form = PasswordChangeForm(user=user)

    context = {
        'form': form,
        'user': user
    }
    
    return render(request, 'users/update_user.html', context)

def update_user(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)

    if request.user.role == 'admin':
        form = CustomUserChangeForm(user=user, data=request.POST)
    
        if form.is_valid():
            form.save() 
            return redirect('users:password_changed', pk=user.pk) #Update after user detail is implemented
        else:
            return render(request, 'users/edit_user.html', {
                'form': form,
                'user': user
        })
    else:
        form = PasswordChangeForm(user=user, data=request.POST)
    
        if form.is_valid():
            form.save() 
            return redirect('users:password_changed', pk=user.pk) #Update after user detail is implemented
        else:
            return render(request, 'users/edit_user.html', {
                'form': form,
                'user': user
        })

#Just to try update_user works. Delete after User Detail is implemented. 
def password_changed_success(request, pk):
    return HttpResponse(f"Password changed successfully for user {pk}!")