from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Custom user to future-proof for fields you may add later.
    For now, rely on AbstractUser fields: username, email, password, etc.
    """
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username or self.email
