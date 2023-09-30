from aiogram.types import Message
from aiogram.dispatcher.filters import Command

from database_tools.Connection import connect
from decorators import command_handler, send_message
from config.ConfigValues import ConfigValues


@command_handler(Command('profile'))
async def profile(message: Message):
    """Отправляет в чат статистику пользователя"""

    stats_values = await (
        await connect.request(
            "SELECT games, points FROM users WHERE user_id = ?",
            (message.from_id,))
    ).fetchone()

    await send_message(
        message.chat.id,
        ConfigValues.profile_message.replace('{games_amount}', str(stats_values[0])).replace('{points_amount}',
                                                                                             str(stats_values[1])))
