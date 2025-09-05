from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    class Roles(models.TextChoices):
        TRAVELER = "traveler", "Traveler"
        ADMIN = "admin", "Admin"

    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.TRAVELER,
    )

    def __str__(self):
        return f"{self.username} ({self.role})"
