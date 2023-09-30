"""
ASGI config for web_django project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

from web_django.chessboards.routing import websocket_urlpatterns as chessboards_websocket_url_patterns
from channels.routing import ProtocolTypeRouter, URLRouter
from web_django.django_log.log import log

os.environ.setdefault('PYTHONASYNCIODEBUG', '1')
os.environ.setdefault('SERVER_GATEWAY_INTERFACE', 'ASGI')

log.info(f'server successful started. Server gateway interface: ASGI')

asgi_application = get_asgi_application()

application = ProtocolTypeRouter({
            "http": asgi_application,
            "websocket": URLRouter(chessboards_websocket_url_patterns)
                       })
