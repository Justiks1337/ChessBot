from DatabaseAssistant import request
from main import main_queue
from typing import Optional
from aiogram.types.message import Message


async def start(message: Message):
	"""Добавляет пользователя в очередь"""

	main_queue.on_new_user(message.from_id)

	await message.reply(
			"Вы успешно зашли в очередь, ожидайте своего противника и уведомления в этом чате! Напоминаю, противник не будет долго вас ждать"
	)


async def profile(message: Message):
	"""Отправляет в чат статистику пользователя"""

	stats_values = await (
		await request(
			"SELECT games, points FROM users WHERE user_id = ?",
			(message.from_id, ))
		).fetchone()

	await message.reply(f"""Ваш профиль 📊📈:
						Осталось игр: {stats_values[0]} ⚔️
						Очков: {stats_values[1]} 💠""")


async def queue_leave(message: Message):
	"""Удаляет пользователя из очереди"""

	main_queue.leave_from_queue(message.from_id)

	await message.reply("Вы успешно покинули очередь!")


async def get_top(message: Message, amount: Optional[int] = None):

	top = await (await request("SELECT user_id, points FROM users ORDER BY points DESC")).fetchall()

	if not amount:
		amount = len(top)

	send_message: str = f"🏆⭐️ Топ {amount} по победам в шахматах: "

	try:
		for player in top[:amount+1]:
			player_name = message.get_
			send_message = send_message + f""

	except IndexError:
		await message.reply(f"Вы указали неверный диапазон участников! (Всего {len(top)} участников)")



