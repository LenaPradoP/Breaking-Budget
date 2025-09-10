from django.urls import path
from .views import ListView, AddExpense, DeleteView



app_name = "expenses"   

urlpatterns = [
    path("", ListView.list_expenses, name="list_expenses"),
    path("new/",AddExpense.new_expense, name="new_expense"),
    path("create/", AddExpense.create_expense, name="create_expense"),
    path("<int:pk>/delete/", DeleteView.delete_expense, name="delete_expense"),

]
