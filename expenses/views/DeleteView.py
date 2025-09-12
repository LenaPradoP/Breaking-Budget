from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from ..models import Expense
from django.contrib import messages


@login_required
def delete_expense(request, pk):
    if request.method == "POST":
        expense_to_delete = get_object_or_404( Expense, pk=pk)
        if request.user.id != expense_to_delete.user.id:
            messages.error(request, "You can only delete your own expenses.")
            return redirect('expenses:list_expenses')
        if expense_to_delete.status != "pending":
            messages.error(request, "Only expenses with status 'pending' can be deleted.")
            return redirect('expenses:list_expenses')
        expense_to_delete.delete()
        messages.success(request, f"Expense {expense_to_delete} has been deleted.")
        return redirect('expenses:list_expenses')
