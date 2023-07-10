#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

import os
import sys

from aiogram import Bot, Dispatcher, executor
from multiprocessing import Process

from config.ConfigValues import ConfigValues

from Game import Game
from telegram.telegram_authorize import authorization_tokens

bot = None
dp = None


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_django.settings')
    try:
        from django.core.management import execute_from_command_line

    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


def start_bot():

    global bot
    global dp

    bot = Bot(token=ConfigValues.telegram_token)
    dp = Dispatcher(bot)

    executor.start_polling(dp)
    print("bot successful started!")


if __name__ == '__main__':
    bot_process = Process(target=start_bot)
    bot_process.start()
    main()
