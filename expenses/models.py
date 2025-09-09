from django.db import models
from django.conf import settings
from datetime import date

# Create your models here.
class Expense(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"
    status = models.CharField(
        max_length=15,               
        choices=Status.choices,
        default=Status.PENDING,
    )
    class Category(models.TextChoices):
        FLIGHT = "flight", "Flight"
        HOTEL = "hotel", "Hotel"
        TRAIN = "train", "Train"
        CAR = "car", "Car"
        TRANSPORTATION = "transportation", "Transportation"
        FOOD = "food", "Food"
        OTHER = "other", "Other"
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.FLIGHT,
    )
    date = models.DateField(default=date.today)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=100, blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,           
        on_delete=models.CASCADE,
        related_name="expenses",
    )

    def __str__(self):
        return f"{self.user_id} - {self.category} - {self.amount} - {self.date}"
    
    class Meta:
        ordering = ["date"]
