from django.db import models
from accounts.models import User


class Friends(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="user")
    friend = models.ForeignKey(User, on_delete=models.CASCADE,related_name="friend")
    status = models.CharField(max_length=50, default="requested")
    request_time = models.DateTimeField(auto_now=True, verbose_name="Requested time")
