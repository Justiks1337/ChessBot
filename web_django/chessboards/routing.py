from .consumers import UserWebsocket
from django.urls import path


websocket_urlpatterns = [
    path('websocket/games/<str:tag>', UserWebsocket.as_asgi())
]
