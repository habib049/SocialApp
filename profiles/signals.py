from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import User
from .models import UserProfile, UserPrivacy


# creating a user profile and user privacy after creation of user
@receiver(post_save, sender=User)
def create_profile(sender, **kwargs):
    print("signal called")
    print(kwargs)
    if kwargs.get('created', False):
        UserProfile.objects.create(user=kwargs['instance'])
        UserPrivacy.objects.create(user=kwargs['instance'])
