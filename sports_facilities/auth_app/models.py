from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('owner', 'Owner'),
        ('admin', 'Admin'),
        ('manager', 'Manager'),
    ]

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='manager',
    )

    # Optional: add any additional fields specific to your app, e.g. profile, contact information, etc.
    contact_number = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.username
