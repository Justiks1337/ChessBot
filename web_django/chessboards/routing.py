from chessboards.consumers import UserWebsocket
from django.urls import path, re_path, utils


websocket_urlpatterns = [
    path('websocket/games/<str:tag>/', UserWebsocket.as_asgi())
]
