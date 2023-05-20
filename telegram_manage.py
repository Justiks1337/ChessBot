from DatabaseAssistant import request
from main import main_queue


async def start(message):
	"""Добавляет пользователя в очередь"""

	main_queue.on_new_user(message.from_id)

	await message.reply(
			"Вы успешно зашли в очередь, ожидайте своего противника и уведомления в этом чате! Напоминаю, противник не будет долго вас ждать"
	)


async def profile(message):
	"""Отправляет в чат статистику пользователя"""

	stats_values = await (
		await request(
			"SELECT games, points FROM users WHERE user_id = ?",
			(message.from_id, ))
		).fetchone()

	await message.reply(f"""Ваш профиль 📊📈:
						Осталось игр: {stats_values[0]} ⚔️
						Очков: {stats_values[1]} 💠""")


async def queue_leave(message):
	"""Удаляет пользователя из очереди"""

	main_queue.leave_from_queue(message.from_id)

	await message.reply("Вы успешно покинули очередь!")
