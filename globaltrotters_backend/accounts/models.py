from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import UserManager


class User(AbstractUser):
    """Matches src/types/auth.ts User: id, fullName, email, avatarUrl?, travelPreferences?"""

    username = None
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=150)
    avatar_url = models.URLField(blank=True, null=True)
    travel_preferences = models.JSONField(blank=True, default=list)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    objects = UserManager()

    def __str__(self):
        return self.email