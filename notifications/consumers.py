import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        if self.scope["user"].is_anonymous:
            self.close()
        else:
            print("consumer user is  : ", self.scope["user"].username)
            self.group_name = str(self.scope["user"].username)
            async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
            self.accept()

    def disconnect(self, close_code):
        self.close()

    def notify(self, event):
        print(event, "notificaiton")
        self.send(text_data=json.dumps(event["text"]))
