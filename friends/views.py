from django.shortcuts import render
import json
from django.views.generic import ListView
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.http import JsonResponse
from .models import Friend, Notification
from accounts.models import User
from .serializers import NotificationSerializer


class FriendList(ListView):
    model = Friend
    context_object_name = "friends"


def send_request(request, username=None):
    if username is not None:
        friend_user = User.objects.get(username=username)
        friend = Friend.objects.create(user=request.user, friend=friend_user)
        notification = Notification.objects.create(type="friend", recipient=friend_user, actor=request.user,
                                                   verb="sent you friend request")
        channel_layer = get_channel_layer()
        channel = "notifications_{}".format(friend_user.username)
        async_to_sync(channel_layer.group_send)(
            channel, {
                "type": "notify",  # method name
                "command": "new_notification",
                "notification": json.dumps(NotificationSerializer(notification).data)
            }
        )
        data = {
            'status': True,
            'message': "Request sent.",
        }
        return JsonResponse(data)
    else:
        pass
