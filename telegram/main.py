from aiogram import Bot, Dispatcher
from config.ConfigValues import ConfigValues
from aiogram.types import Message
from Queue import Queue
from telegram_manage import start, profile, queue_leave
from telegram_log.log import log


bot = Bot(token=ConfigValues.telegram_token)
dp = Dispatcher(bot)
main_queue = Queue()
log.info('bot successful started!')


@dp.message_handler(commands=['start'])
async def start_command_handler(message: Message):
	"""Добавляет человека в очередь"""

	await start(message)


@dp.message_handler(commands=['profile'])
async def profile_command_handler(message: Message):
	"""Сендит профиль автора сообщения"""

	await profile(message)


@dp.message_handler(commands=['queue_leave'])
async def profile_command_handler(message: Message):
	"""Убирает автора команды из очереди"""

	await queue_leave(message)
