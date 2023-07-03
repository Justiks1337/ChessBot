from aiogram import Bot
from aiogram.types import Message
from telegram_core import in_blacklist
from Queue import main_queue
from config.ConfigValues import ConfigValues


@in_blacklist
async def queue_join(bot: Bot, message: Message):
	"""Добавляет пользователя в очередь"""

	main_queue.add_new_user(message.from_id)

	await bot.send_message(message.chat.id, ConfigValues.on_queue_join_message)


@in_blacklist
async def queue_leave(bot: Bot, message: Message):
	"""Удаляет пользователя из очереди"""

	main_queue.leave_from_queue(message.from_id)

	await bot.send_message(message.chat.id, ConfigValues.on_queue_leave_message)
