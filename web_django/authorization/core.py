from uuid import uuid4

from config.ConfigValues import ConfigValues
from database_tools.Connection import connect
from web_django.manage import bot


async def fill_data(user_id: int):
    await __download_user_avatar(user_id)

    data = await bot.get_chat_member(chat_id=user_id, user_id=user_id)
    user_nickname = f'{data.user.first_name} {data.user.last_name}'
    username = data.user.username
    session_id = new_session_id()

    await connect.request(
        "INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)", (
            user_id,
            ConfigValues.games_amount,
            0,
            user_nickname,
            username,
            session_id))


async def __download_user_avatar(user_id: int):
    """Download user profile photo

    :arg user_id - user id
    """

    user_profile_photo = await bot.get_user_profile_photos(user_id)

    if len(user_profile_photo.photos) > 0:

        file = await bot.get_file(user_profile_photo.photos[0][0].file_id)
        await bot.download_file(file.file_path, f'../avatars/{user_id}.png')


def new_session_id():
    session_id = str(uuid4())

    return session_id
