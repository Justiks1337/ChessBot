"""
ASGI config for web_django project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django import setup
from django.core.management import call_command
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from channels.sessions import SessionMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_django.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
setup()


asgi_application = get_asgi_application()

from chessboards.routing import websocket_urlpatterns as chessboards_websocket_url_patterns
from django_log.log import log

os.environ.setdefault('PYTHONASYNCIODEBUG', '1')
os.environ.setdefault('SERVER_GATEWAY_INTERFACE', 'ASGI')

call_command('makemigrations')
call_command('migrate')

log.info(f'server successful started. Server gateway interface: ASGI')

application = ProtocolTypeRouter({
            "http": asgi_application,
            "websocket": AllowedHostsOriginValidator(
                SessionMiddlewareStack(URLRouter(chessboards_websocket_url_patterns)))
                       })
