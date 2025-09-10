from django.urls import path
from .views import ListView, DeleteView

app_name = "expenses"   

urlpatterns = [
    path("", ListView.list_expenses, name="list_expenses"),
    path("<int:pk>/delete/", DeleteView.delete_expense, name="delete_expense"),
]
