from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.template.defaultfilters import slugify


class User(AbstractUser):
    slug = models.SlugField(unique=True, null=True)
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

    def get_absolute_url(self):
        return reverse('profile:user_profile', kwargs={'username': self.username})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)
        super(User, self).save(*args, **kwargs)
