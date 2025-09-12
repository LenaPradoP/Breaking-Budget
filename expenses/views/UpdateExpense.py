from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, render,get_object_or_404
from ..models import Expense
from ..forms import ExpenseWebCreateForm




@login_required
def edit_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    form = ExpenseWebCreateForm(instance=expense)
    context = {
        'expense': expense,
        'form': form,
       
    }
    return render(request, 'expenses/update.html', context)

@login_required
def update_expense(request, pk):
    if request.method == 'POST':
        expense = get_object_or_404(Expense, pk=pk,user=request.user)
        form = ExpenseWebCreateForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('expenses:list_expenses')
    

    return redirect('expenses:edit_expense', pk=pk)
