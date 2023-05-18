from aiogram import Bot, Dispatcher
from config import tg_bot_token
from aiogram.types import Message
from Queue import Queue
from telegram_manage import start, profile, queue_leave


bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)
main_queue = Queue()


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
