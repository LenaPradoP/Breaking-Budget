
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


@login_required
def delete_user(request, pk):
    #in django admin is a superuser
    if not request.user.is_superuser: 
        return redirect ('users:list_users')
        
    user = get_object_or_404( User, pk=pk)
    #admins can't delete themselves
    if request.user == user:
        return redirect('users:list_users')

    user.delete()
    return redirect('users:list_users')