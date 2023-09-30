from sqlite3 import IntegrityError

from aiogram.types import Message
from aiogram.dispatcher.filters import Command

from database_tools.Connection import connect
from config.ConfigValues import ConfigValues
from decorators import in_admins, command_handler, send_message


@command_handler(command=Command('add_on_blacklist'))
@in_admins
async def add_on_blacklist(message: Message):

	try:
		username = message.get_args().replace('@', '')
		await connect.request("INSERT INTO blacklist VALUES ((SELECT user_id FROM users WHERE username = ?), ?)", (
			username, username))

	except IntegrityError:
		await send_message(message.chat.id, ConfigValues.on_invalid_args)
		return

	await send_message(message.chat.id, ConfigValues.successful_add_to_blacklist.replace('{username}', username))


@command_handler(command=Command('remove_from_blacklist'))
@in_admins
async def remove_from_blacklist(message: Message):

	try:
		user_id = int(message.get_args())
	except ValueError:
		await send_message(message.chat.id, ConfigValues.on_invalid_args)
		return

	await connect.request("DELETE FROM blacklist WHERE user_id = ?", (user_id, ))

	await send_message(message.chat.id, ConfigValues.successful_remove_from_blacklist)
