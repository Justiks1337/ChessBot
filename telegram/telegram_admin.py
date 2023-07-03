from config.ConfigValues import ConfigValues
from aiogram import Bot
from aiogram.types import Message
from database_tools.Connection import connect
from sqlite3 import IntegrityError


def in_admins(func):
	"""Check user in admins"""
	async def wrapped(*args, **kwargs):
		if str(args[1].from_id) in ConfigValues.admin_ids:
			return await func(*args, **kwargs)

		return await args[0].send_message(args[1].chat.id, ConfigValues.on_is_not_admin)

	return wrapped


@in_admins
async def add_on_blacklist(bot: Bot, message: Message):

	try:
		username = message.get_args().replace('@', '')
		await connect.request("INSERT INTO blacklist VALUES ((SELECT user_id FROM users WHERE username = ?), ?)", (
			username, username))

	except IntegrityError:
		await bot.send_message(message.chat.id, ConfigValues.on_invalid_args)
		return

	await bot.send_message(message.chat.id, ConfigValues.successful_add_to_blacklist.replace('{username}', username))


@in_admins
async def remove_from_blacklist(bot: Bot, message: Message):

	try:
		user_id = int(message.get_args())
	except ValueError:
		await bot.send_message(message.chat.id, ConfigValues.on_invalid_args)
		return

	await connect.request("DELETE FROM blacklist WHERE user_id = ?", (user_id, ))

	await bot.send_message(message.chat.id, ConfigValues.successful_remove_from_blacklist)


