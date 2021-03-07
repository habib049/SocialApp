import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from notifications import routing as notification_routing
from chat import routing as chat_routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socialApp.settings')

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            notification_routing.websocket_urlpatterns+
            chat_routing.websocket_urlpatterns,
        )),
})
