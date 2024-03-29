from aiogram import Dispatcher, Bot

from config.ConfigValues import ConfigValues

bot: Bot = Bot(token=ConfigValues.telegram_token)
dp = Dispatcher()
