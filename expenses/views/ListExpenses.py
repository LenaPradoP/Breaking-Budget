from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from ..models import Expense, CustomUser


@login_required
def list_expenses(request):

    if not request.user.is_authenticated:
        raise PermissionDenied
    role = getattr(request.user, "role", None)
    is_admin = (
        (hasattr(CustomUser, "Role") and role == CustomUser.Role.ADMIN) or (role == "admin")
    )
    if not is_admin:
        raise PermissionDenied
    expenses = Expense.objects.all().order_by("status")

    context = {
        "expenses": expenses,
    }
    
    return render(request, 'users/list_users.html', context)