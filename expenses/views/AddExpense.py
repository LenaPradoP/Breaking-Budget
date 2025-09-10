from django.shortcuts import render, redirect
from ..forms import ExpenseWebCreateForm
from django.contrib.auth.decorators import login_required
from ..models import Expense

@login_required

def new_expense(request):
    form = ExpenseWebCreateForm()
    context = {
    'new_expense_form': form
}
    return render(request, 'expenses/new.html', context)


def create_expense(request):
 new_expense = None
 if request.method == "POST":
    new_expense = ExpenseWebCreateForm(request.POST)
    if new_expense.is_valid():
        new_expense.status = 'pending'
        new_expense.save()
    return redirect('expenses:list_expenses')
 else: 
        new_expense = ExpenseWebCreateForm()
 return render(request, 'expenses/new.html', {'expense': new_expense})
 

