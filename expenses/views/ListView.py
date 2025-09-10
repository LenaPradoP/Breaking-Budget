from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from ..models import Expense
from ..forms import ExpensesFilterForm

@login_required
def list_expenses(request):

    if request.user.role == 'admin' or request.user.is_superuser:
        expenses = Expense.objects.all().order_by("status")
    elif request.user.role == 'traveler':
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
        if form.cleaned_data['category']:
            expenses = expenses.filter(category=form.cleaned_data['category'])

        if form.cleaned_data['status']:
            expenses = expenses.filter(status=form.cleaned_data['status'])

        # Admin-only: "Only my expenses"
        if form.cleaned_data.get('mine') and request.user.role == 'admin':
            expenses = expenses.filter(user=request.user)
        
        if form.cleaned_data['order_by']:
            expenses = expenses.order_by(form.cleaned_data['order_by'])
    
    return form, expenses
