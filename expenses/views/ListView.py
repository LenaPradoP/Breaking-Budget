from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from ..models import Expense

@login_required
def list_expenses(request):

    if request.user.role == 'admin':
        expenses = Expense.objects.all().order_by("status")
    elif request.user.role == 'traveler':
        expenses = Expense.objects.filter(user_id=request.user.pk).order_by("status")
    else:
        raise PermissionDenied("You don't have permission to see this page")

    context = {
        "expenses": expenses,
    }
    
    return render(request, 'expenses/list_expenses.html', context)