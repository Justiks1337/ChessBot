from database_tools.Connection import connect
from config.ConfigValues import ConfigValues
from asyncio import sleep, create_task


def in_blacklist(func):
    """Check user in blacklist"""

    async def wrapped(*args, **kwargs):
        if (await (
                await connect.request("SELECT user_id FROM blacklist WHERE username = ?", (args[1].from_user.username,))
        ).fetchone()):
            return await args[0].send_message(args[1].chat.id, ConfigValues.on_blacklist_message)

        return await func(*args, **kwargs)

    return wrapped


def authorize(func):
    async def wrapper(bot, message):
        user = await(
            await connect.request("SELECT user_id FROM users WHERE user_id = ?", (message.from_id,))).fetchone()
        if not user:
            await bot.send_message(message.chat.id, ConfigValues.unauthorized_message)
            return

        return await func(bot, message)

    return wrapper


def recharge(func):
    async def wrapper(bot, message):
        if message.from_id in users_in_recharge:
            await bot.send_message(message.chat.id, ConfigValues.in_recharge)
            return

        users_in_recharge.append(message.from_id)
        sleep_task = create_task(clear_recharge(message.from_id))
        func_task = create_task(func(bot, message))
        await sleep_task
        await func_task

    return wrapper


async def clear_recharge(user_id: int):
    await sleep(ConfigValues.recharge_time)
    users_in_recharge.remove(user_id)


users_in_recharge = []
