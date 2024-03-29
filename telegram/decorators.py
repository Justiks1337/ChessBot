from asyncio import sleep, create_task

import aiogram

from telegram.database import Connection
from config.ConfigValues import ConfigValues
from telegram import dp, bot


def in_blacklist(func):
    """Check user in blacklist"""

    async def wrapped(message: aiogram.types.Message):
        if await Connection().connection.fetchrow(
                "SELECT user_id FROM blacklist WHERE username = $1",
                message.from_user.username):

            return await send_message(message.chat.id, ConfigValues.on_blacklist_message)

        return await func(message)

    return wrapped


def authorize(func):
    async def wrapper(message: aiogram.types.Message):
        user = await Connection().connection.fetchrow(
            "SELECT user_id FROM users WHERE user_id = $1",
            message.from_user.id)

        if not user:
            await send_message(message.chat.id, ConfigValues.unauthorized_message)
            return

        return await func(message)

    return wrapper


def in_admins(func):
    """Check user in admins"""
    async def wrapped(message):
        if str(message.from_user.id) in ConfigValues.admin_ids:
            return await func(message)

        return await send_message(message.chat.id, ConfigValues.on_is_not_admin)

    return wrapped


def recharge(func):
    async def wrapper(message):
        if message.from_user.id in users_in_recharge:
            return await send_message(message.chat.id, ConfigValues.in_recharge)

        users_in_recharge.append(message.from_user.id)
        sleep_task = create_task(clear_recharge(message.from_user.id))
        func_task = create_task(func(message))
        await sleep_task
        await func_task

    return wrapper


def only_in_dm(coro):
    async def wrapper(message: aiogram.types.Message):
        if message.from_user.id != message.chat.id:
            return await send_message(message.chat.id, ConfigValues.only_in_dm_message)

        await coro(message)

    return wrapper


def command_handler(command):
    def decorator(coro):
        @dp.message(command)
        @only_in_dm
        @recharge
        @authorize
        @in_blacklist
        async def wrapper(message: aiogram.types.Message):
            await coro(message)

        return wrapper
    return decorator


async def clear_recharge(user_id: int):
    await sleep(ConfigValues.recharge_time)
    users_in_recharge.remove(user_id)


async def send_message(chat_id: int, text: str, *args, **kwargs):
    await bot.send_message(chat_id, text, *args, **kwargs)


users_in_recharge = []
