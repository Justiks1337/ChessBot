from asyncio import sleep, create_task

import aiogram

from database_tools.Connection import connect
from config.ConfigValues import ConfigValues
from telegram import dp, bot


def in_blacklist(func):
    """Check user in blacklist"""

    async def wrapped(message):
        if (await (
                await connect.request("SELECT user_id FROM blacklist WHERE username = ?", (message.from_user.username,))
        ).fetchone()):
            return await send_message(message.chat.id, ConfigValues.on_blacklist_message)

        return await func(message)

    return wrapped


def authorize(func):
    async def wrapper(message):
        user = await(
            await connect.request("SELECT user_id FROM users WHERE user_id = ?", (message.from_id,))).fetchone()
        if not user:
            await send_message(message.chat.id, ConfigValues.unauthorized_message)
            return

        return await func(message)

    return wrapper


def in_admins(func):
    """Check user in admins"""
    async def wrapped(message):
        if str(message.from_id) in ConfigValues.admin_ids:
            return await func(message)

        return await send_message(message.chat.id, ConfigValues.on_is_not_admin)

    return wrapped


def recharge(func):
    async def wrapper(message):
        if message.from_id in users_in_recharge:
            return await send_message(message.chat.id, ConfigValues.in_recharge)

        users_in_recharge.append(message.from_id)
        sleep_task = create_task(clear_recharge(message.from_id))
        func_task = create_task(func(message))
        await sleep_task
        await func_task

    return wrapper


def only_in_dm(coro):
    async def wrapper(message: aiogram.types.Message):
        if message.from_id != message.chat.id:
            return await send_message(message.chat.id, ConfigValues.only_in_dm_message)

        await coro(message)

    return wrapper


def command_handler(command: aiogram.dispatcher.filters.Command):
    def decorator(coro):
        @dp.message_handler(command)
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
