from aiogram import Bot, Dispatcher, executor
from config.ConfigValues import ConfigValues
from aiogram.types import Message
from telegram_manage import start, profile, queue_leave, get_top, queue_join, authorization
from telegram_log.log import log
from aiogram.dispatcher.filters import Command


bot = Bot(token=ConfigValues.telegram_token)
dp = Dispatcher(bot)

log.info('bot successful started!')


@dp.message_handler(Command('start'))
async def start_command_handler(message: Message):
	pass


@dp.message_handler(Command('profile'))
async def profile_command_handler(message: Message):
	"""Сендит профиль автора сообщения"""

	await profile(bot, message)


@dp.message_handler(Command('queue_join'))
async def queue_join_command_handler(message: Message):
	"""Добавляет человека в очередь"""

	await queue_join(bot, message)


@dp.message_handler(Command('queue_leave'))
async def queue_leave_command_handler(message: Message):
	"""Убирает автора команды из очереди"""

	await queue_leave(bot, message)


@dp.message_handler(Command('dashboard'))
async def dashboard_handler(message: Message):
	"""Отправляет пользователю топ игроков"""

	await get_top(bot, message)

executor.start_polling(dp)
