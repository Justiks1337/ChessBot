from asyncio import get_event_loop

from aiogram import Dispatcher, Bot

from config.ConfigValues import ConfigValues

bot: Bot = Bot(token=ConfigValues.telegram_token)
dp = Dispatcher(bot, loop=get_event_loop())
