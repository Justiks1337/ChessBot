#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

import os
from asyncio import run

from aiogram import Bot

from web_django.django_log.log import log

from config.ConfigValues import ConfigValues


bot = Bot(token=ConfigValues.telegram_token)


def main():
    """Run administrative tasks."""



    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_django.web_django.settings')

    log.info("worker successful started")


async def on_exit():
    """"""

    session = await bot.get_session()
    await session.close()


if __name__ == '__main__':

    main()

    run(on_exit())
