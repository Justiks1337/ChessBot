from aiogram.types import Message
from aiogram.filters import Command

from Queue import main_queue as queue
from config.ConfigValues import ConfigValues
from decorators import command_handler, send_message


@command_handler(Command('play'))
async def queue_join(message: Message):
	"""Добавляет пользователя в очередь"""

	await queue.add_new_user(message.from_user.id)


@command_handler(Command('leave'))
async def queue_leave(message: Message):
	"""Удаляет пользователя из очереди"""

	try:
		queue.leave_from_queue(message.from_user.id)
	except KeyError:
		await send_message(message.chat.id, ConfigValues.if_not_in_queue)
		return

	await send_message(message.chat.id, ConfigValues.on_queue_leave_message)


async def send_url_to_playground(user_id: int, uuid):
	"""send url to game"""

	await send_message(
		user_id,
		ConfigValues.on_find_enemy.replace('{url}', ConfigValues.url_to_playground.replace('{rout}', uuid)))
