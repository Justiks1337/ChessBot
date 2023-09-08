from .consumers import BotConsumer
from django.urls import path


websocket_urlpatterns = [
    path('websocket/bot_consumer', BotConsumer.as_asgi())
]
