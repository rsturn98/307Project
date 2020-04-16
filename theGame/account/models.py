from django.db import models
import os

# Create your models here.
class Character(models.Model):
    image_url = models.ImageField()

    def __str__(self):
        return self.image_url.url
