from sqlite3 import IntegrityError

from aiogram.types import Message
from aiogram.filters import Command

from config.ConfigValues import ConfigValues
from decorators import in_admins, command_handler, send_message
from telegram.database import Connection


@command_handler(Command('add_on_blacklist'))
@in_admins
async def add_on_blacklist(message: Message):

	try:
		username = message.get_args().replace('@', '')
		await Connection.connection.execute(
			"INSERT INTO blacklist VALUES ((SELECT user_id FROM users WHERE username = $1), $2)",
			username,
			username)

	except IntegrityError:
		await send_message(message.chat.id, ConfigValues.on_invalid_args)
		return

	await send_message(message.chat.id, ConfigValues.successful_add_to_blacklist.replace('{username}', username))


@command_handler(Command('remove_from_blacklist'))
@in_admins
async def remove_from_blacklist(message: Message):

	try:
		user_id = int(message.get_args())
	except ValueError:
		await send_message(message.chat.id, ConfigValues.on_invalid_args)
		return

	await Connection().connection.execute("DELETE FROM blacklist WHERE user_id = ?", (user_id, ))

	await send_message(message.chat.id, ConfigValues.successful_remove_from_blacklist)
