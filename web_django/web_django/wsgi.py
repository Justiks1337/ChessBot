"""
WSGI config for web_django project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_django.web_django.settings')
os.environ.setdefault('SERVER_GATEWAY_INTERFACE', 'WSGI')

