from aiogram.types import Message
from aiogram.filters import Command

from decorators import in_blacklist, recharge, only_in_dm
from authorization_core import download_user_avatar, send_auth_message
from telegram import dp


@dp.message(Command('start'))
@recharge
@only_in_dm
@in_blacklist
async def start(message: Message):
	"""send start message"""

	await send_auth_message(message)
	await download_user_avatar(message.from_user.id)
