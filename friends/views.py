from django.views.generic import ListView
from rest_framework.generics import ListAPIView
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.http import JsonResponse
from .models import Friend
from accounts.models import User
from notifications.models import Notification
from .pagination import FriendListPagination
from .serializers import UserSerializer


class FriendList(ListView):
    model = Friend
    context_object_name = "friends"
    template_name = 'home/friends.html'
    paginate_by = 6

    def get_queryset(self):
        return Friend.objects.filter(
            user=self.request.user, status="friend"
        ).select_related(
            'friend'
        )

    def get_context_data(self, **kwargs):
        context = super(FriendList, self).get_context_data(**kwargs)
        requested = Friend.objects.filter(user=self.request.user, status="requested").count()
        context['requested'] = requested
        return context


class RequestFriendList(ListView):
    model = Friend
    context_object_name = 'requested_friend'
    paginate_by = 6

    def get_queryset(self):
        return Friend.objects.filter(
            user=self.request.user, status="requested"
        ).select_related(
            'friend'
        )


def send_friend_request(request):
    if request.method == 'POST' and request.is_ajax():
        user_id = request.POST['userId']
        receiver = User.objects.get(id=user_id)
        sender = request.user
        message_note = "sends you a friend request"
        notification_type = "friend"

        if not Notification.objects.filter(sender=sender, receiver=receiver, type=notification_type).exists():
            # notification = Notification.objects.create(type=notification_type, sender=sender, receiver=receiver,
            #                                            note=message_note)
            # notification.save()

            # notify user in real time
            data = {
                'sender': sender.username,
                'receiver': receiver.username,
                'imageUrl': sender.user_profile.profile_image.url,
                'message': message_note,
                'type': 'friend'
            }

            channel_layer = get_channel_layer()

            async_to_sync(channel_layer.group_send)(
                str(receiver.username),
                {
                    "type": "notify",
                    "text": data,
                },
            )

            return JsonResponse({'notify': True})

        return JsonResponse({'notify': False})


def accept_friend_request(request):
    print('in functions')
    if request.method == 'POST' and request.is_ajax():
        username = request.POST['username']
        receiver = User.objects.get(username=username)
        sender = request.user
        message_note = "accept your friend request"
        notification_type = "friend accept"

        # updating database
        # friend = Friend.objects.get(user=sender, friend=receiver, status='requested')
        # friend.status = 'friend'
        # friend.save()
        #
        # notification = Notification.objects.create(type=notification_type, sender=sender, receiver=receiver,
        #                                            note=message_note)
        # notification.save()

        # generating notification in realtime
        data = {
            'sender': sender.username,
            'receiver': receiver.username,
            'imageUrl': sender.user_profile.profile_image.url,
            'message': message_note,
            'type': 'friend'
        }

        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            str(receiver.username),
            {
                "type": "notify",
                "text": data,
            },
        )

        return JsonResponse({'notify': True})
