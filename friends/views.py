from django.shortcuts import render
import json
from django.views.generic import ListView
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.http import JsonResponse
from .models import Friend
from accounts.models import User
from notifications.models import Notification


class FriendList(ListView):
    model = Friend
    context_object_name = "friends"


def send_request(request):
    if request.method == 'POST' and request.is_ajax():
        user_id = request.POST['userId']
        receiver = User.objects.get(id=user_id)
        friend = Friend.objects.create(user=request.user, friend=receiver)
        friend.save()
        notification = Notification.objects.create(type="friend", receiver=receiver, sender=request.user,
                                                   note="sent you friend request")
        notification.save()

        channel_layer = get_channel_layer()

        channel = "notifications_{}".format(receiver.username)

        async_to_sync(channel_layer.group_send)(
            channel, {
                "type": "notifications.notify",  # method name
                "command": "new_notification",
            }
        )
        data = {
            'status': True,
            'message': "Request sent.",
        }
        return JsonResponse(data)
    else:
        pass


def view(request):
    if request.is_ajax():
        user_id = request.POST['userId']
        receiver = User.objects.get(id=user_id)

        print("receiver is : ", receiver.username)
        current_user = request.user

        channel_layer = get_channel_layer()

        data = "notification" + "...."

        async_to_sync(channel_layer.group_send)(
            str(receiver.username),  # Channel Name, Should always be string
            {
                "type": "notify",  # Custom Function written in the consumers.py
                "text": data,
            },
        )

    return JsonResponse({'res': 1})
