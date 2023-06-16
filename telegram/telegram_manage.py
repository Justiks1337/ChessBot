from database_tools.Connection import connect
from Queue import main_queue
from aiogram.types.message import Message
from aiogram.bot.bot import Bot


async def start(bot: Bot, message: Message):
	pass


async def queue_join(bot: Bot, message: Message):
	"""Добавляет пользователя в очередь"""

	main_queue.add_new_user(message.from_id)

	await bot.send_message(
		message.chat.id,
		"Вы успешно зашли в очередь, ожидайте своего противника и уведомления в этом чате! \n \n \
		Напоминаю, противник не будет долго вас ждать"
	)


async def profile(bot: Bot, message: Message):
	"""Отправляет в чат статистику пользователя"""

	stats_values = await (
		await connect.request(
			"SELECT games, points FROM users WHERE user_id = ?",
			(message.from_id, ))
		).fetchone()

	await bot.send_message(
		message.chat.id,
		f"Ваш профиль 📊📈: \n \n Осталось игр: {stats_values[0]} ⚔️ \n Очков: {stats_values[1]} 💠")


async def queue_leave(bot: Bot, message: Message):
	"""Удаляет пользователя из очереди"""

	main_queue.leave_from_queue(message.from_id)

	await bot.send_message(message.chat.id, "Вы успешно покинули очередь!")


async def get_top(bot: Bot, message: Message):
	"""send message with dashboard"""

	amount = message.get_args()

	top = await (await connect.request("SELECT user_id, points FROM users ORDER BY points DESC")).fetchall()

	if not amount:
		amount = 10

	if amount == "all":
		amount = len(top)

	msg: str = f"🏆⭐️ Топ {amount} по победам в шахматах: \n \n"

	try:
		position = 0
		for player in top[:int(amount)]:

			position += 1
			player_name = (await bot.get_chat_member(player[0], player[0])).user.username

			msg = msg + f"{position}. @{player_name}: {player[1]} очков \n"

	except IndexError:
		await message.reply(f"Вы указали неверный диапазон участников! (Всего {len(top)} участников)")

	await bot.send_message(message.chat.id, msg)


async def authorization(bot: Bot, message: Message):
	"""Authorization command"""

	pass
