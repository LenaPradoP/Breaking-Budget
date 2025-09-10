from django.urls import path
from .views import ListView, DeleteView, ReviewExpense

app_name = "expenses"   

urlpatterns = [
    path("", ListView.list_expenses, name="list_expenses"),
    path("<int:pk>/delete/", DeleteView.delete_expense, name="delete_expense"),
    path("status/<int:pk>/", ReviewExpense.update_expense_status, name="update_expense_status"),
]
