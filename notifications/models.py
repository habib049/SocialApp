from django.db import models
from django.conf import settings
from accounts.models import User


class Notification(models.Model):
    type = models.CharField(default="friend", max_length=50)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notification_sender')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                 related_name="notification_receiver")
    note = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    time_stamp = models.DateTimeField(auto_now=True, verbose_name="Requested time")
    seen = models.BooleanField(default=False)
