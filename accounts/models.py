from typing import override

from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Role (models.TextChoices):
        ADMIN = "admin", "Admin"
        STAFF = "staff", "Staff"

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.STAFF)

    updated_by = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="users_updated"
    )
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="users_created"
    )

    @override
    def __str__(self):
        return self.username
