from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        MANAGER = "MANAGER", "Manager"
        STAFF = "STAFF", "Staff"

    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.STAFF)

    def __str__(self):
        return f"{self.username} ({self.role})"