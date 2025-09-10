from django.contrib import admin
from .models import Expense
# Register your models here.

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "category", "date", "amount", "description", "user" )
    list_filter = ("status", "category", "date", "user")
    search_fields = ("description", "user__username", "user__email")
    ordering = ("-date",) #ordering has to be a tuple, the - is to do descending order
