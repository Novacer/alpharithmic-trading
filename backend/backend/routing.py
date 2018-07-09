from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url
from . import consumers

websocket_urlpatterns = [
    url(r'^ws/chat/(?P<room_name>[^/]+)/$', consumers.ChatConsumer),
]

application = ProtocolTypeRouter({
    "websocket" : URLRouter(websocket_urlpatterns)
})
