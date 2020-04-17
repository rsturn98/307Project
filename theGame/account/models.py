from django.db import models
from django.contrib.auth.models import User
import os

# Create your models here.
class Character(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    image_url = models.CharField(max_length=200, default=1)

    def __str__(self):
        return self.image_url
