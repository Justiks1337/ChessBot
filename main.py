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


@dp.callback_query_handler()
async def send_welcome(callback_query: aiogram.types.CallbackQuery):
	await bot.answer_callback_query(callback_query.id, url="127.0.0.1:8000")


aiogram.executor.start_polling(dp)
