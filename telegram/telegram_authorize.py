from asyncio import sleep

from aiogram import Bot
from aiogram.types import Message
from aiohttp import ClientSession

from config.ConfigValues import ConfigValues
from database_tools.Connection import connect
from telegram.telegram_core import recharge


authorization_tokens = {}


@recharge
async def new_token(bot: Bot, message: Message):

	user_id = message.from_id

	async with ClientSession() as session:
		async with session.post(
				f"http://{ConfigValues.server_ip}:{ConfigValues.server_port}/api/v1/new_token?user_id={user_id}",
				headers={"content-type": "application/json", "Authorization": ConfigValues.server_authkey}) as response:

			json = await response.json()

			if json['success']:

				await bot.send_message(message.chat.id, ConfigValues.authorization_message.replace('{code}', json['token']), parse_mode='HTML')
				await sleep(ConfigValues.authorization_tokens_live_time)

				await delete_token(bot, message)
				return

			await bot.send_message(message.chat.id, ConfigValues.on_duplicate_authorization_code)


async def delete_token(bot: Bot, message: Message):
	async with ClientSession() as session:
		async with session.post(
			f"http://{ConfigValues.server_ip}:{ConfigValues.server_port}/api/v1/delete_token?user_id={message.from_id}",
			headers={'Authorization': ConfigValues.server_authkey, "content-type": "application/json"},
		) as response:
			if (await response.json())['success']:
				await bot.send_message(message.chat.id, ConfigValues.on_delete_authorization_code)


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
