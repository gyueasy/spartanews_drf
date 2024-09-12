from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    nickname = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    nickname = models.CharField(max_length=20, unique=True)
    introduction = models.TextField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile/', null=True, blank=True)