
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

User = get_user_model() 


@login_required

def user_detail(request, pk):

    user = get_object_or_404(User, pk = pk)


    if request.user.role.name.lower() == "admin":
        context = {

            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "email": user.email,
            "role": user.role.name
        }
        return render(request, 'users/user_detail.html', context)
    
    if request.user.pk == pk:

        return {
            "first_name": request.first_name,
            "last_name": request.last_name,
            "username": request.username,
            "email": request.email,
          

        }
    return render(request, 'users/user_detail.html', context)


