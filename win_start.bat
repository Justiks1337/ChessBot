set PYTHONPATH=.
set DJANGO_SETTINGS_MODULE=web_django.web_django.settings
start /b daphne web_django.web_django.asgi:application &
start /b python telegram/main.py &