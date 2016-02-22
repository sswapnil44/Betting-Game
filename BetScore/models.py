from django.db import models
from football.models import UserProfile

# Create your models here.

class Users(models.Model):
    email = models.EmailField(unique=True)
    auth_key = models.TextField(default=None, max_length=100)
