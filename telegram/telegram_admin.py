import aiohttp
from aiogram.types import Message
from aiogram.filters import Command

from config.ConfigValues import ConfigValues
from decorators import in_admins, command_handler, send_message


@command_handler(Command('add_on_blacklist'))
@in_admins
async def add_on_blacklist(message: Message):
	user_id = int(message.get_args())
	async with aiohttp.ClientSession() as session:
		async with session.post(
				f"{ConfigValues.server_http_protocol}://{ConfigValues.server_ip}/blacklist/add_to_blacklist",
				params={"user_id": user_id},
				headers={
					"content-type": "application/json",
					"Authorization": ConfigValues.server_authkey}):
			await send_message(message.chat.id, ConfigValues.successful_add_to_blacklist.replace('{username}', user_id))


@command_handler(Command('remove_from_blacklist'))
@in_admins
async def remove_from_blacklist(message: Message):
	user_id = int(message.get_args())

	async with aiohttp.ClientSession() as session:
		async with session.post(
				f"{ConfigValues.server_http_protocol}://{ConfigValues.server_ip}/blacklist/remove_from_blacklist",
				params={"user_id": user_id},
				headers={"Content-type": "application/json",
						 "Authorization": ConfigValues.server_authkey}):
			await send_message(message.chat.id, ConfigValues.successful_remove_from_blacklist)

