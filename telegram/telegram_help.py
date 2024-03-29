from aiogram.types import Message
from aiogram.filters import Command

from decorators import recharge, send_message
from config.ConfigValues import ConfigValues
from telegram import dp


@dp.message(Command('help'))
@recharge
async def send_manual(message: Message):
    await send_message(message.chat.id, ConfigValues.manual)
