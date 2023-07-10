from aiogram.types import Message
from aiogram import Bot
from database_tools.Connection import connect
from telegram.telegram_core import in_blacklist, authorize, recharge
from config.ConfigValues import ConfigValues


@recharge
@authorize
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
                ConfigValues.profile_message.replace('{games_amount}', str(stats_values[0])).replace('{points_amount}', str(stats_values[1])))
