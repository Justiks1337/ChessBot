import asyncpg

from config.ConfigValues import ConfigValues
from main import Connection
from telegram import bot


async def __download_user_avatar(user_id: int):
    """Download user profile photo

    :arg user_id - user id
    """

    user_profile_photo = await bot.get_user_profile_photos(user_id)

    if len(user_profile_photo.photos) > 0:
        file = await bot.get_file(user_profile_photo.photos[0][0].file_id)
        file_destination = get_destination(user_id, get_file_name(file.file_path))
        await bot.download_file(file.file_path, file_destination)


def get_file_name(file_path: str) -> str:
    return file_path[-file_path[::-1].index('/'):]


def get_file_format(file_name: str) -> str:
    return file_name[file_name.index('.'):]


def get_destination(user_id: int, file_name) -> str:
    file_format = get_file_format(file_name)

    file_destination = ConfigValues.path_to_avatars + str(user_id) + file_format

    return file_destination


async def new_data(user_id: int):
    data = await bot.get_chat_member(chat_id=user_id, user_id=user_id)
    user_nickname = data.user.first_name
    if data.user.last_name:
        user_nickname = user_nickname + f" {data.user.last_name}"

    username = data.user.username

    connect = Connection()
    try:
        await connect.connection.execute(
            """INSERT INTO users VALUES (
                $1, $2, $3, $4, $5, $6, $7)""",
            user_id,
            ConfigValues.games_amount,
            0,
            user_nickname,
            username,
            None,
            None)
    except asyncpg.UniqueViolationError:
        return False

    await __download_user_avatar(user_id)
