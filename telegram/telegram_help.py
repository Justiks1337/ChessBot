from config.ConfigValues import ConfigValues
from telegram_core import recharge
from aiogram import Bot
from aiogram.types import Message


@recharge
async def send_manual(bot: Bot, message: Message):
    await bot.send_message(message.chat.id, ConfigValues.manual)
