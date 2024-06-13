import aiohttp
from aiogram.types import Message
from aiogram.exceptions import TelegramForbiddenError
from aiogram.filters import Command

from config.ConfigValues import ConfigValues
from decorators import command_handler, send_message


@command_handler(Command('top'))
async def get_top(message: Message):
    """send message with dashboard"""

    count = message.get_args()

    amount = 0

    if not count:
        amount = 10
    elif isinstance(count, int):
        amount = int(count)
    elif count == "all":
        amount = 0

    async with aiohttp.ClientSession() as session:
        async with session.post(
                f"{ConfigValues.server_http_protocol}://{ConfigValues.server_ip}/api/v1/dashboard",
                params={"count": count},
                headers={"Content-type": "application/json",
                         "Authorization": ConfigValues.server_authkey}) as response:
            top = await response.json()

    msg: str = ConfigValues.dashboard_title.replace('{amount}', str(amount))

    position = 0
    for player in top:
        try:

            if not player.get("username"):
                player_name = player[3]
            else:
                player_name = player[2]

            position += 1

            msg = msg + ConfigValues.dashboard_object.replace(
                '{position}', str(position)).replace(
                '{player_name}', f'<a href="tg://user?id={player.get("user_id")}">{player_name}</a>').replace(
                '{points_amount}', str(player.get("points")))

        except TelegramForbiddenError:
            continue

    await send_message(message.chat.id, msg, parse_mode="html")

