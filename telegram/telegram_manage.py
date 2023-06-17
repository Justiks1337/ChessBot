from database_tools.Connection import connect
from Queue import main_queue
from aiogram.types.message import Message
from aiogram.bot.bot import Bot
from aiogram.utils.exceptions import ChatNotFound
from config.ConfigValues import ConfigValues


async def start(bot: Bot, message: Message):
	if await (await connect.request("SELECT user_id FROM users WHERE user_id = ?", (message.from_id, ))).fetchone():
		await bot.send_message(message.chat.id, ConfigValues.game_instructions)
		return

	await bot.send_message(message.chat.id, ConfigValues.authorization_instructions)


async def profile(bot: Bot, message: Message):
	"""Отправляет в чат статистику пользователя"""

	stats_values = await (
		await connect.request(
			"SELECT games, points FROM users WHERE user_id = ?",
			(message.from_id, ))
		).fetchone()

	await bot.send_message(
		message.chat.id,
		ConfigValues.profile_message.replace('{games_amount}', stats_values[0]).replace('{points_amount}', stats_values[1]))


async def queue_join(bot: Bot, message: Message):
	"""Добавляет пользователя в очередь"""

	main_queue.add_new_user(message.from_id)

	await bot.send_message(message.chat.id, ConfigValues.on_queue_join_message)


async def queue_leave(bot: Bot, message: Message):
	"""Удаляет пользователя из очереди"""

	main_queue.leave_from_queue(message.from_id)

	await bot.send_message(message.chat.id, ConfigValues.on_queue_leave_message)


async def get_top(bot: Bot, message: Message):
	"""send message with dashboard"""

	amount = message.get_args()

	top = await (await connect.request("SELECT user_id, points FROM users ORDER BY points DESC")).fetchall()

	if not amount:
		amount = 10

	if amount == "all":
		amount = len(top)

	msg: str = ConfigValues.dashboard_title.replace('{amount}', str(amount))

	try:
		position = 0
		for player in top[:int(amount)]:
			try:

				player_name = (await bot.get_chat_member(player[0], player[0])).user.username
				position += 1

				msg = msg + ConfigValues.dashboard_object.replace(
					'{position}', str(position)).replace(
					'{player_name}', player_name).replace(
					'{points_amount}', str(player[1]))

			except ChatNotFound:
				continue

	except IndexError:
		await bot.send_message(message.chat.id, ConfigValues.dashboard_on_range_error.replace('{amount}', len(top)))

	await bot.send_message(message.chat.id, msg)


async def authorization(bot: Bot, message: Message):
	"""Authorization command"""

	pass
