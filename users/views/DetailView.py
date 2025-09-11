
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.core.exceptions import PermissionDenied
from ..models import CustomUser

User = get_user_model()

@login_required
def user_detail(request, pk):
    # Hide superusers
    target_user = get_object_or_404(User, pk=pk, is_superuser=False)

    # Allow: self, admins, or superusers viewing others
    is_self = request.user.pk == target_user.pk
    is_admin = request.user.role == User.Role.ADMIN
    is_super = request.user.is_superuser

    if is_self or is_admin or is_super:
        context = {"user": target_user}
        return render(request, "users/detail_view.html", context)

    raise PermissionDenied("You don't have permission to see this page")
