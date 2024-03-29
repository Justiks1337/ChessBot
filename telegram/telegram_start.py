from aiogram.types import Message
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types.inline_keyboard_button import InlineKeyboardButton

from decorators import in_blacklist, recharge, only_in_dm
from config.ConfigValues import ConfigValues
from telegram import dp


@dp.message(Command('start'))
@recharge
@only_in_dm
@in_blacklist
async def start(message: Message):
	"""send start message"""

	await message.reply(ConfigValues.authorization_instructions)
