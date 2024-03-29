from aiogram.types import Message
from aiogram.filters import Command

from decorators import command_handler, send_message
from config.ConfigValues import ConfigValues
from telegram.database import Connection


@command_handler(Command('profile'))
async def profile(message: Message):
    """Отправляет в чат статистику пользователя"""

    stats_values = await Connection().connection.fetchrow(
            "SELECT games, points FROM users WHERE user_id = $1",
            message.from_user.id)

    await send_message(
        message.chat.id,
        ConfigValues.profile_message.replace('{games_amount}', str(stats_values[0])).replace('{points_amount}',
                                                                                             str(stats_values[1])))
