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

    if not amount:
        amount = 10

    try:

        int(amount)
        top = await (await connect.request(f"SELECT user_id, points, username, nickname FROM users ORDER BY points DESC LIMIT {amount}")).fetchall()

    except ValueError:

        if amount == "all":
            top = await (await connect.request("SELECT user_id, points, username, nickname FROM users ORDER BY points DESC")).fetchall()
            amount = len(top)

        else:
            await send_message(message.chat.id, ConfigValues.on_invalid_args)
            return

    msg: str = ConfigValues.dashboard_title.replace('{amount}', str(amount))

    position = 0
    for player in top:
        try:

            if not player[2]:
                player_name = player[3]
            else:
                player_name = player[2]

            position += 1

            msg = msg + ConfigValues.dashboard_object.replace(
                '{position}', str(position)).replace(
                '{player_name}', f'<a href="tg://user?id={player[0]}">{player_name}</a>').replace(
                '{points_amount}', str(player[1]))

        except ChatNotFound:
            continue

    await send_message(message.chat.id, msg, parse_mode="html")

