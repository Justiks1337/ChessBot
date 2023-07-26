from asyncio import sleep

from aiogram import Bot
from aiogram.types import Message
from aiohttp import ClientSession

from config.ConfigValues import ConfigValues
from telegram_core import recharge


authorization_tokens = {}


@recharge
async def new_token(bot: Bot, message: Message):

	user_id = message.from_id

	async with ClientSession() as session:
		async with session.post(
				f"http://{ConfigValues.server_ip}:{ConfigValues.server_port}/api/v1/new_token",
				params={"user_id": user_id},
				headers={"content-type": "application/json", "Authorization": ConfigValues.server_authkey}) as response:

			json = await response.json()

			if json['success']:

				await bot.send_message(message.chat.id, ConfigValues.authorization_message.replace('{code}', json['token']), parse_mode='MARKDOWN')
				await sleep(ConfigValues.authorization_tokens_live_time)

				await delete_token(bot, message)
				return

			await bot.send_message(message.chat.id, ConfigValues.on_duplicate_authorization_code)


async def delete_token(bot: Bot, message: Message):
	async with ClientSession() as session:
		async with session.post(
			f"http://{ConfigValues.server_ip}:{ConfigValues.server_port}/api/v1/delete_token",
			params={"user_id": message.from_id},
			headers={'Authorization': ConfigValues.server_authkey, "content-type": "application/json"},
		) as response:
			if (await response.json())['success']:
				await bot.send_message(message.chat.id, ConfigValues.on_delete_authorization_code)
