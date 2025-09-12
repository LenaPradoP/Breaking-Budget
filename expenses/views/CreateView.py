from django.shortcuts import render, redirect
from ..forms import ExpenseWebCreateForm
from django.contrib.auth.decorators import login_required
from ..models import Expense

@login_required
def new_expense(request):
    form = ExpenseWebCreateForm()
    return render(request, "expenses/new.html", {"form": form})

@login_required
def create_expense(request):
    if request.method != "POST":
        return redirect("expenses:new_expense")

    form = ExpenseWebCreateForm(request.POST)
    if form.is_valid():
        expense = form.save(commit=False)   
        expense.user = request.user      
        expense.status = Expense.Status.PENDING
        expense.save()                  
        return redirect("expenses:list_expenses")
    return render(request, "expenses/new.html", {"form": form})
