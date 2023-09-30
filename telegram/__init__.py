from asyncio import get_event_loop

from aiogram import Dispatcher

from config.ConfigValues import ConfigValues
from Bot import Bot

bot: Bot = Bot(token=ConfigValues.telegram_token)
dp = Dispatcher(bot, loop=get_event_loop())
