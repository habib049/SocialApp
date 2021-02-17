import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncJsonWebsocketConsumer, WebsocketConsumer
from django.contrib.auth import get_user_model
# from django.core import serializers
# from .serializers import NotificationSerializer
# from .models import Notification

User = get_user_model()


# class FriendRequestConsumer(AsyncJsonWebsocketConsumer):
#     async def fetch_messages(self):
#         user = self.scope['user']
#         notifications = Notification.objects.select_related('actor').filter(recipient=user, type="friend")
#         serializer = NotificationSerializer(notifications, many=True)
#         content = {
#             'command': 'notifications',
#             'notifications': json.dumps(serializer.data)
#         }
#
#         await self.send_json(content)
#
#     def notifications_to_json(self, notifications):
#         result = []
#         for notification in notifications:
#             result.append(self.notification_to_json(notification))
#         return result
#
#     @staticmethod
#     def notification_to_json(notification):
#         return {
#             'actor': serializers.serialize('json', [notification.actor]),
#             'recipient': serializers.serialize('json', [notification.recipient]),
#             'verb': notification.verb,
#             'created_at': str(notification.timestamp)
#         }
#
#     async def connect(self):
#         user = self.scope['user']
#         grp = 'notifications_{}'.format(user.username)
#         await self.channel_layer.group_add(grp, self.channel_name)
#         await self.accept()
#
#     async def disconnect(self, close_code):
#         user = self.scope['user']
#         grp = 'notifications_{}'.format(user.username)
#         await self.channel_layer.group_discard(grp, self.channel_name)
#
#     async def notify(self, event):
#         await self.send_json(event)
#
#     async def receive(self, text_data=None, bytes_data=None, **kwargs):
#         data = json.loads(text_data)
#         if data['command'] == 'fetch_friend_notifications':
#             await self.fetch_messages()
#


class NotificationConsumer(WebsocketConsumer):

    # Function to connect to the websocket
    def connect(self):
        # Checking if the User is logged in
        if self.scope["user"].is_anonymous:
            # Reject the connection
            self.close()
        else:
            print("consumer user is  : ",self.scope[
                                      "user"].username)
            # print(self.scope["user"])   # Can access logged in user details by using self.scope.user, Can only be used if AuthMiddlewareStack is used in the routing.py
            self.group_name = str(self.scope[
                                      "user"].username)  # Setting the group name as the pk of the user primary key as it is unique to each user. The group name is used to communicate with the user.
            async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
            self.accept()

    # Function to disconnet the Socket
    def disconnect(self, close_code):
        self.close()
        # pass

    # Custom Notify Function which can be called from Views or api to send message to the frontend
    def notify(self, event):
        print(event, "notificaiton")
        self.send(text_data=json.dumps(event["text"]))
