from aiogram import Bot
from aiogram.types import Message
from Queue import main_queue
from config.ConfigValues import ConfigValues
from telegram_core import in_blacklist


@in_blacklist
async def queue_join(bot: Bot, message: Message):
	"""Добавляет пользователя в очередь"""

	await main_queue.add_new_user(bot, message.from_id)


@in_blacklist
async def queue_leave(bot: Bot, message: Message):
	"""Удаляет пользователя из очереди"""

	main_queue.leave_from_queue(message.from_id)

	await bot.send_message(message.chat.id, ConfigValues.on_queue_leave_message)


async def send_url_to_playground(bot: Bot, user_id: int, uuid):
	"""send url to game"""

	await bot.send_message(
		user_id,
		ConfigValues.on_find_enemy.replace('{url}', ConfigValues.url_to_playground.replace('{rout}', uuid)))
