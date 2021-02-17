import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter


from friends import routing as notification_routing
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socialApp.settings')

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            notification_routing.websocket_urlpatterns
        )),
})
