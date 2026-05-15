from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    # Remove first_name and last_name
    first_name = None
    last_name = None

    # Add custom fields
    name = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'auth_user'