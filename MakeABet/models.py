from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import smart_text

class UserProfile(models.Model):
    #Links UserProfile to User model
    user = models.OneToOneField(User)

    points = models.IntegerField(default=0)

    def __str__(self):
        return smart_text(self.user.username)
