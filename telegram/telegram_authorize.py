from asyncio import sleep

from aiogram.types import Message
from aiogram.dispatcher.filters import Command
from aiohttp import ClientSession

from config.ConfigValues import ConfigValues
from decorators import recharge, send_message
from telegram import dp


@dp.message_handler(Command("authorization"))
@recharge
async def new_token(message: Message):
    user_id = message.from_id

    async with ClientSession() as session:
        async with session.post(
                f"{ConfigValues.server_http_protocol}://{ConfigValues.server_ip}:{ConfigValues.server_port}/api/v1/new_token",
                params={"user_id": user_id},
                headers={"content-type": "application/json", "Authorization": ConfigValues.server_authkey}) as response:
            json = await response.json()

            if json['success']:
                await send_message(
                    message.chat.id, ConfigValues.authorization_message.replace('{code}', json['token']
                                                                                ).replace('{url}',
                f"{ConfigValues.proxy_http_protocol}://{ConfigValues.proxy_ip}/authorization/"),
                    parse_mode='MARKDOWN')
                await sleep(ConfigValues.authorization_tokens_live_time)

                await delete_token(message)
                return

            await send_message(message.chat.id, ConfigValues.on_authorization_error)


async def delete_token(message: Message):
    async with ClientSession() as session:
        async with session.post(
                f"{ConfigValues.server_http_protocol}://{ConfigValues.server_ip}:{ConfigValues.server_port}/api/v1/delete_token",
                params={"user_id": message.from_id},
                headers={'Authorization': ConfigValues.server_authkey, "content-type": "application/json"},
        ) as response:
            if (await response.json())['success']:
                await send_message(message.chat.id, ConfigValues.on_delete_authorization_code)
