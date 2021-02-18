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
        return Friend.objects.filter(user=self.request.user, status="friend")

    def get_context_data(self, **kwargs):
        context = super(FriendList, self).get_context_data(**kwargs)
        requested = Friend.objects.filter(user=self.request.user, status="requested").count()
        context['requested'] = requested
        return context


class FriendListApiView(ListAPIView):
    pagination_class = FriendListPagination

    def get_queryset(self):
        return Friend.objects.filter(user=self.request.user, status="friend")

    def list(self, request):
        queryset = self.get_queryset()

        page = self.paginate_queryset(queryset)
        response_list = self.get_paginated_response(page)
        print(response_list)
        serializer = UserSerializer(response_list, many=True)
        requested = Friend.objects.filter(user=self.request.user, status="requested").count()
        return JsonResponse({'friends': serializer.data, 'requested': requested})


class RequestedListApiView(ListAPIView):
    pagination_class = FriendListPagination

    def get_queryset(self):
        return Friend.objects.filter(user=self.request.user, status="requested")

    def list(self, request):
        queryset = self.get_queryset()
        serializer = UserSerializer(queryset, many=True)
        # append serializer's data with some additional value
        response_list = serializer.data
        return JsonResponse({'friends': response_list})


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
                'message': message_note
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
