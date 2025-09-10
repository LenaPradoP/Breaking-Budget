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
    return render(request, 'expenses/new.html', {"form": form})

@login_required
def create_expense(request):
 form = None
 if request.method == "POST":
    form = ExpenseWebCreateForm(request.POST)
    if form.is_valid():
        expense = form.save(commit=False)
        expense.user = request.user     
        expense.status = 'pending'
        form.save()
    return redirect('expenses:list_expenses')
 else: 
        form = ExpenseWebCreateForm()
 return render(request, 'expenses/new.html', {'form': form})
 
