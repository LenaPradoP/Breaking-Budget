
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.core.exceptions import PermissionDenied

User = get_user_model() 


@login_required

def user_detail(request, pk):
    user = get_object_or_404(User, pk = pk)
    if request.user.pk == pk:
        context = {
            "user": user
            }
        return render(request, 'users/detail_view.html', context)
    elif request.user.role == 'admin':
        context = {
            "user": user
            }
        return render(request, 'users/detail_view.html', context)
    else:
        raise PermissionDenied
        
