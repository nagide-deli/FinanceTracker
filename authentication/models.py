from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    REQUIRED_FIELDS = ['full_name']
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email


# Create your models here.
