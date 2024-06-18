import aiohttp
from aiogram.types import Message
from aiogram.filters import Command

from decorators import command_handler, send_message
from config.ConfigValues import ConfigValues


@command_handler(Command('profile'))
async def profile(message: Message):
    """Отправляет в чат статистику пользователя"""

    async with aiohttp.ClientSession() as session:
        async with session.get(
                f"{ConfigValues.server_http_protocol}://{ConfigValues.server_ip}/api/v1/profile/{message.from_user.id}/",
                headers={"Content-type": "application/json",
                         "Authorization": ConfigValues.server_authkey}) as response:
            stats_values = await response.json()

    await send_message(
        message.chat.id,
        ConfigValues.profile_message.replace('{points_amount}', str(stats_values["points"])))
