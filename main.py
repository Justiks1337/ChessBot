import aiogram
from config import tg_bot_token


bot = aiogram.Bot(tg_bot_token)
dp = aiogram.Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_command(message):
	await message.answer(text="Тест пон типа да")


@dp.message_handler(commands=['top'])
async def start_command(message):
	await message.answer(text="Тест пон типа да")


aiogram.executor.start_polling(dp)
