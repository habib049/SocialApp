from django.db import models
from django.conf import settings
from accounts.models import User


class Friend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friend")
    status = models.CharField(max_length=50, default="requested")
    request_time = models.DateTimeField(auto_now=True, verbose_name="Requested time")
