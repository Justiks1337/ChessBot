"""
ASGI config for web_django project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from whitenoise import WhiteNoise

from web_django.chessboards.routing import websocket_urlpatterns
from channels.routing import ProtocolTypeRouter, URLRouter
from web_django.django_log.log import log
from web_django.web_django.wsgi import application as wsgi_app

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_django.web_django.settings')
os.environ.setdefault('PYTHONASYNCIODEBUG', '1')
os.environ.setdefault('SERVER_GATEWAY_INTERFACE', 'ASGI')

log.info(f'server successful started. Server gateway interface: ASGI')

asgi_application = get_asgi_application()

application = ProtocolTypeRouter({
            "http": asgi_application,
            "websocket": URLRouter(websocket_urlpatterns)
                       })


WN = WhiteNoise(wsgi_app, root='web_django/static/')
