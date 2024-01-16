#!/bin/bash
export PYTHONPATH=.
export DJANGO_SETTINGS_MODULE=web_django.web_django.settings
daphne web_django.web_django.asgi:application -b 127.0.0.1 -p 8080&
python3 telegram/main.py&
