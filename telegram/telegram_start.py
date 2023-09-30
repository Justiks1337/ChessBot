from aiogram.types import Message
from aiogram.dispatcher.filters import Command
from aiogram.types.reply_keyboard import KeyboardButton, ReplyKeyboardMarkup

from decorators import in_blacklist, recharge, only_in_dm
from config.ConfigValues import ConfigValues
from telegram import dp


@dp.message_handler(Command('start'))
@recharge
@only_in_dm
@in_blacklist
async def start(message: Message):
	"""send start message"""

	await message.reply(
		ConfigValues.authorization_instructions,
		reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('/authorization 🔑')))
