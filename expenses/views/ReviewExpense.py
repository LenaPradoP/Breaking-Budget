# expenses/views/ReviewExpense.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from users.models import CustomUser

from ..models import Expense

@login_required
def update_expense_status(request, pk):
    if request.method != "POST":
        return redirect("expenses:list_expenses")

    expense = get_object_or_404(Expense, pk=pk)
    new_status = request.POST.get("status")

    valid_status = {Expense.Status.PENDING, Expense.Status.APPROVED, Expense.Status.REJECTED}
    if new_status not in valid_status:
        messages.error(request, "Invalid status.")
        return redirect("expenses:list_expenses")

    # Admins: only if expense status is pending, and only to approved/rejected
    if request.user.role == CustomUser.Role.ADMIN:
        if expense.status != Expense.Status.PENDING:
            messages.error(request, "Admins can only change pending expenses.")
            return redirect("expenses:list_expenses")
        if new_status not in (Expense.Status.APPROVED, Expense.Status.REJECTED):
            messages.error(request, "Admins can only review pending expenses.")
            return redirect("expenses:list_expenses")
        expense.status = new_status
        expense.save(update_fields=["status"])
        messages.success(request, f"Expense {expense.pk} set to {new_status}.")
        return redirect("expenses:list_expenses")

    messages.error(request, "Not allowed.")
    return redirect("expenses:list_expenses")
