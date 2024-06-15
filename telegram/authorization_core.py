import os
import aiohttp
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiohttp.client import ClientSession

from config.ConfigValues import ConfigValues
from decorators import send_message
from telegram import bot


async def download_user_avatar(user_id: int):
    """Download user profile photo

    :arg user_id - user id
    """

    user_profile_photo = await bot.get_user_profile_photos(user_id)

    if len(user_profile_photo.photos) > 0:
        file = await bot.get_file(user_profile_photo.photos[0][0].file_id)
        file_destination = get_destination(user_id, get_file_name(file.file_path))
        await bot.download_file(file.file_path, file_destination)

        with open(file_destination, "rb") as destination:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                        f"{ConfigValues.server_http_protocol}://{ConfigValues.server_ip}/api/v1/add_avatar?file_name={file_destination}",
                        data={"file": destination},
                        headers={"Authorization": ConfigValues.server_authkey}):
                    os.remove(file_destination)


def get_file_name(file_path: str) -> str:
    return file_path[-file_path[::-1].index('/')]


def get_file_format(file_name: str) -> str:
    try:
        return file_name[file_name.index('.'):]
    except ValueError:
        return ".png"


def get_destination(user_id: int, file_name) -> str:
    print(file_name)
    file_format = get_file_format(file_name)

    file_destination = str(user_id) + file_format

    return file_destination


async def send_auth_message(message: Message):
    user_id = message.from_user.id

    async with ClientSession() as session:
        async with session.post(
                f"{ConfigValues.server_http_protocol}://{ConfigValues.server_ip}/api/v1/new_token",
                params={"user_id": user_id,
                        "username": message.from_user.username,
                        "nickname": message.from_user.full_name},
                headers={"content-type": "application/json",
                         "Authorization": ConfigValues.server_authkey}) as response:
            json = dict(await response.json())
            if json['success']:

                button = InlineKeyboardButton(
                    text="Авторизуйся!",
                    url=f"{ConfigValues.proxy_http_protocol}://{ConfigValues.proxy_ip}/?token={json['token']}")
                markup = InlineKeyboardMarkup(inline_keyboard=[[button]])

                await message.reply(ConfigValues.authorization_message, reply_markup=markup)
                return

            await send_message(message.chat.id, ConfigValues.on_authorization_error)

