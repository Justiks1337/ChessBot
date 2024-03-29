#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

import sys
from asyncio import run

from aiogram import Bot

from config.ConfigValues import ConfigValues


bot = Bot(token=ConfigValues.telegram_token)


def main():
    """Run administrative tasks."""

    try:
        from django.core.management import execute_from_command_line
        execute_from_command_line(sys.argv)
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc


async def on_exit():
    """"""

    session = await bot.get_session()
    await session.close()


if __name__ == '__main__':

    main()

    run(on_exit())
