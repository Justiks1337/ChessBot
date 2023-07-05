from uuid import uuid4
from asyncio import sleep
from aiogram import Bot
from aiogram.types import Message
from config.ConfigValues import ConfigValues
from database_tools.Connection import connect
from telegram_core import recharge


authorization_tokens = {}


@recharge
async def new_token(bot: Bot, message: Message):

	token = str(uuid4())

	try:
		authorization_tokens[message.from_id]  # Check in authorization_tokens (if not raise KeyError)
		await bot.send_message(message.chat.id, ConfigValues.on_duplicate_authorization_code)
		return

	except KeyError:
		authorization_tokens[message.from_id] = token
		await bot.send_message(message.chat.id, ConfigValues.authorization_message.replace('{code}', token), parse_mode='HTML')

	await sleep(300)
	delete_token(message.from_id)
	await bot.send_message(message.chat.id, ConfigValues.on_delete_authorization_code)


def delete_token(user_id):
	try:
		del authorization_tokens[user_id]
	except KeyError:
		pass  # pass to avoid spam in console


async def fill_data(bot: Bot, user_id: int):
	await __download_user_avatar(bot, user_id)

	data = await bot.get_chat_member(chat_id=user_id, user_id=user_id)
	user_nickname = f'{data.user.first_name} {data.user.last_name}'
	username = data.user.username

	await connect.request(
		"INSERT INTO users VALUES (?, ?, ?, ?, ?)", (
			user_id,
			ConfigValues.games_amount,
			0,
			user_nickname,
			username))


async def __download_user_avatar(bot: Bot, user_id: int):
	"""Download user profile photo

	:arg bot - bot object
	:arg user_id - user id
	"""

	user_profile_photo = await bot.get_user_profile_photos(user_id)

	if len(user_profile_photo.photos) > 0:

		file = await bot.get_file(user_profile_photo.photos[0][0].file_id)
		await bot.download_file(file.file_path, f'../avatars/{user_id}.png')


