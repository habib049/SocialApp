from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    gender = models.CharField(max_length=50, null=True, choices=[
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    ])
    about = models.TextField(null=True, blank=True, verbose_name="About")

    def __unicode__(self):
        return self.username

    def __str__(self):
        return self.username
