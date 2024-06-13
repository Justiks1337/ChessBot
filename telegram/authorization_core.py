import os
import aiohttp

from config.ConfigValues import ConfigValues
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

