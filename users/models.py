from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        TRAVELER = "traveler", "Traveler"
        ADMIN = "admin", "Admin"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.TRAVELER,
    )

    def __str__(self):
        return f"{self.username} ({self.role})"
