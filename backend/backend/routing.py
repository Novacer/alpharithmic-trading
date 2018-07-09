from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url
from . import consumers

websocket_urlpatterns = [
    url(r'^ws/logs/(?P<room_name>[^/]+)/$', consumers.LogsConsumer),
]

application = ProtocolTypeRouter({
    "websocket" : URLRouter(websocket_urlpatterns)
})
