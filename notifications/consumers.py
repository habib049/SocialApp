import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer, WebsocketConsumer
from django.contrib.auth import get_user_model
from django.core import serializers
from .serializers import NotificationSerializer
from .models import Notification

User = get_user_model()


class FriendRequestConsumer(AsyncJsonWebsocketConsumer):
    async def fetch_messages(self):
        user = self.scope['user']
        notifications = Notification.objects.select_related('actor').filter(recipient=user, type="friend")
        serializer = NotificationSerializer(notifications, many=True)
        content = {
            'command': 'notifications',
            'notifications': json.dumps(serializer.data)
        }

        await self.send_json(content)

    def notifications_to_json(self, notifications):
        result = []
        for notification in notifications:
            result.append(self.notification_to_json(notification))
        return result

    @staticmethod
    def notification_to_json(notification):
        return {
            'actor': serializers.serialize('json', [notification.actor]),
            'recipient': serializers.serialize('json', [notification.recipient]),
            'verb': notification.verb,
            'created_at': str(notification.timestamp)
        }

    async def connect(self):
        user = self.scope['user']
        grp = 'notifications_{}'.format(user.username)
        await self.channel_layer.group_add(grp, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        user = self.scope['user']
        grp = 'notifications_{}'.format(user.username)
        await self.channel_layer.group_discard(grp, self.channel_name)

    async def notify(self, event):
        await self.send_json(event)

    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        data = json.loads(text_data)
        if data['command'] == 'fetch_friend_notifications':
            await self.fetch_messages()


class NotificationConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        user = self.scope['user']
        grp = 'notifications_{}'.format(user.username)
        print("group at connect is ",grp)
        await self.channel_layer.group_add(grp, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        user = self.scope['user']
        grp = 'notifications_{}'.format(user.username)
        await self.channel_layer.group_discard(grp, self.channel_name)

    async def notify(self, event):
        print("in function")
        print(event)
        await self.send_json(event)

    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        data = json.loads(text_data)
        print(data)
