from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from ..models import Expense
from ..forms import ExpensesFilterForm
from users.models import CustomUser

@login_required
def list_expenses(request):

    if request.user.role == CustomUser.Role.ADMIN:
        expenses = Expense.objects.all().order_by("status")
    elif request.user.role == CustomUser.Role.TRAVELER:
        expenses = Expense.objects.filter(user_id=request.user.pk).order_by("status")
    else:
        raise PermissionDenied("You don't have permission to see this page")
    
    form, expenses = apply_expenses_filters_and_ordering(request, expenses)

    context = {
        "expenses": expenses,
        "form": form
    }
    
    return render(request, 'expenses/list_expenses.html', context)

def apply_expenses_filters_and_ordering(request, initial_queryset):
    """
    Helper function that applies filters and ordering to an existing queryset.
    
    Args:
        request: HttpRequest object
        initial_queryset: The base queryset to filter/order
    
    Returns:
        tuple: (form, filtered_queryset)
    """
    form = ExpensesFilterForm(request.GET)
    
    expenses = initial_queryset
    
    if form.is_valid():
        category = form.cleaned_data.get('category')
        status   = form.cleaned_data.get('status')
        mine     = form.cleaned_data.get('mine')
        order_by = form.cleaned_data.get('order_by') or 'status'  # fallback

        if category:
            expenses = expenses.filter(category=category)

        if status:
            expenses = expenses.filter(status=status)

        # Admin-only: "Only my expenses"
        if mine and request.user.role == CustomUser.Role.ADMIN:
            expenses = expenses.filter(user=request.user)

        expenses = expenses.order_by(order_by)

    return form, expenses
