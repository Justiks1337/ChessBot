from aiogram.types import Message
from aiogram.utils.exceptions import ChatNotFound
from aiogram.dispatcher.filters import Command

from database_tools.Connection import connect
from config.ConfigValues import ConfigValues
from decorators import command_handler, send_message
from telegram import bot


@command_handler(Command(['dashboard', 'top']))
async def get_top(message: Message):
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
		await send_message(message.chat.id, ConfigValues.on_invalid_args)

	msg: str = ConfigValues.dashboard_title.replace('{amount}', str(amount))

	position = 0
	for player in top[:int(amount)+1]:
		try:

			user = (await bot.get_chat_member(player[0], player[0])).user

			if not user.username:
				player_name = user.first_name
				if user.last_name:
					player_name = player_name + f" {user.last_name}"
			else:
				player_name = f"@{user.username}"

			position += 1

			msg = msg + ConfigValues.dashboard_object.replace(
				'{position}', str(position)).replace(
				'{player_name}', player_name).replace(
				'{points_amount}', str(player[1]))

		except ChatNotFound:
			continue

	await send_message(message.chat.id, msg)
