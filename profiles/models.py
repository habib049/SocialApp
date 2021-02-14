from django.db import models
from accounts.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    profile_image = models.ImageField(upload_to='profile/', default='profile/default_profile.jpg')
    cover_image = models.ImageField(upload_to='cover/', default='cover/default_cover.jpg')
    date_of_birth = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.user.username

    def get_username(self):
        return self.user.username


class UserEducation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_education')
    degree = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    is_complete = models.BooleanField(default=True)
    is_public = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username

    def get_username(self):
        return self.user.username


class Hobby(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='hobby_image/')


class UserHobby(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_hobby')
    hobby = models.ForeignKey(Hobby, on_delete=models.CASCADE, related_name="hobby")

    def get_username(self):
        return self.user.username

    def get_hobby_name(self):
        return self.hobby.name


class UserPrivacy(models.Model):
    PRIVACY_OPTIONS = [
        ('friend', 'Friends'),
        ('public', 'Public (Any one)'),
        ('me', 'Only me')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_privacy')
    profile_image = models.CharField(max_length=50, choices=PRIVACY_OPTIONS, default='public')
    date_of_birth = models.CharField(max_length=50, choices=PRIVACY_OPTIONS, default='public')
    phone_number = models.CharField(max_length=50, choices=PRIVACY_OPTIONS, default='public')
    friends = models.CharField(max_length=50, choices=PRIVACY_OPTIONS, default='public')
    search = models.CharField(max_length=50, choices=PRIVACY_OPTIONS, default='public')

    def get_username(self):
        return self.user.username
