set PYTHONPATH=.
set DJANGO_SETTINGS_MODULE=web_django.web_django.settings
start /b daphne web_django.web_django.asgi:application -b 192.168.1.60 -p 8000 &
start /b python telegram/main.py &