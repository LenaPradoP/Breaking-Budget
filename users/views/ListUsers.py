from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from ..models import CustomUser

@login_required
def view_users(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
    role = getattr(request.user, "role", None)
    is_admin = (
        (hasattr(CustomUser, "Role") and role == CustomUser.Role.ADMIN) or (role == "admin")
    )
    if not is_admin:
        raise PermissionDenied
    users = CustomUser.objects.all().order_by("username")
    return render(request, 'users/list_users.html', {"users" : users})
