from database_tools.Connection import connect
from Queue import main_queue
from aiogram.types.message import Message
from aiogram.bot.bot import Bot
from aiogram.utils.exceptions import ChatNotFound
from config.ConfigValues import ConfigValues
from telegram_core import download_user_avatar, in_blacklist, in_admins
from uuid import uuid4
from sqlite3 import IntegrityError


@in_blacklist
async def start(bot: Bot, message: Message):
	"""send start message"""

	if await (await connect.request("SELECT user_id FROM users WHERE user_id = ?", (message.from_id, ))).fetchone():
		await bot.send_message(message.chat.id, ConfigValues.game_instructions)
		return

	await bot.send_message(message.chat.id, ConfigValues.authorization_instructions)


@in_blacklist
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


@in_blacklist
async def get_top(bot: Bot, message: Message):
	"""send message with dashboard"""

	amount = message.get_args()

	top = await (await connect.request("SELECT user_id, points FROM users ORDER BY points DESC")).fetchall()

	if not amount:
		amount = 10

	if amount == "all":
		amount = len(top)

	try:
		int(amount)

	except ValueError:
		await bot.send_message(message.chat.id, ConfigValues.on_invalid_args)

	msg: str = ConfigValues.dashboard_title.replace('{amount}', str(amount))

	position = 0
	for player in top[:int(amount)+1]:
		try:

			player_name = (await bot.get_chat_member(player[0], player[0])).user.username
			position += 1

			msg = msg + ConfigValues.dashboard_object.replace(
				'{position}', str(position)).replace(
				'{player_name}', player_name).replace(
				'{points_amount}', str(player[1]))

		except ChatNotFound:
			continue

	await bot.send_message(message.chat.id, msg)


@in_blacklist
async def authorization(bot: Bot, message: Message):
	"""Authorization command"""

	if (
		await(
			await connect.request(
				"SELECT user_id FROM authorization WHERE user_id = ?",
				(message.from_id, ))
			).fetchone()):

		await bot.send_message(message.chat.id, ConfigValues.on_duplicate_authorization_code)
		return

	code = str(uuid4())
	user_nickname = f'{message.from_user.first_name} {message.from_user.last_name}'
	user_name = message.from_user.username

	await download_user_avatar(bot, message.from_id)

	await connect.request("INSERT INTO authorization VALUES (?, ?, ?, ?)", (
		message.from_id,
		user_nickname,
		user_name,
		code))

	await bot.send_message(message.chat.id, ConfigValues.authorization_message.replace('{code}', code), parse_mode='HTML')


@in_admins
async def add_on_blacklist(bot: Bot, message: Message):

	try:
		username = message.get_args().replace('@', '')
		await connect.request("INSERT INTO blacklist VALUES ((SELECT user_id FROM users WHERE username = ?), ?)", (
			username, username))

	except IntegrityError:
		await bot.send_message(message.chat.id, ConfigValues.on_invalid_args)
		return

	await bot.send_message(message.chat.id, ConfigValues.successful_add_to_blacklist.replace('{username}', username))


@in_admins
async def remove_from_blacklist(bot: Bot, message: Message):

	try:
		user_id = int(message.get_args())
	except ValueError:
		await bot.send_message(message.chat.id, ConfigValues.on_invalid_args)
		return

	await connect.request("DELETE FROM blacklist WHERE user_id = ?", (user_id, ))

	await bot.send_message(message.chat.id, ConfigValues.successful_remove_from_blacklist)
