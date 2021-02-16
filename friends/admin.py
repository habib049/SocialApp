from django.contrib import admin
from .models import Friend


@admin.register(Friend)
class FriendAdmin(admin.ModelAdmin):
    fields = ['user', 'friend', 'request_time']
