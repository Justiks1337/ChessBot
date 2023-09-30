from sqlite3 import IntegrityError

from asgiref.sync import sync_to_async
from django.http import HttpRequest
from ipware import get_client_ip

from config.ConfigValues import ConfigValues
from database_tools.Connection import connect
from web_django.manage import bot


async def fill_data(user_id: int):
    try:
        return await new_data(user_id)

    except IntegrityError:
        pass


async def __download_user_avatar(user_id: int):
    """Download user profile photo

    :arg user_id - user id
    """

    user_profile_photo = await bot.get_user_profile_photos(user_id)

    if len(user_profile_photo.photos) > 0:

        file = await bot.get_file(user_profile_photo.photos[0][0].file_id)
        file_destination = get_destination(user_id, get_file_name(file.file_path))
        await bot.download_file(file.file_path, destination=file_destination)


def get_file_name(file_path: str) -> str:
    return file_path[-file_path[::-1].index('/'):]


def get_file_format(file_name: str) -> str:
    return file_name[file_name.index('.'):]


def get_destination(user_id: int, file_name) -> str:

    file_format = get_file_format(file_name)

    file_destination = ConfigValues.path_to_avatars + str(user_id) + file_format

    return file_destination.encode('ascii')


async def new_data(user_id: int):
    data = await bot.get_chat_member(chat_id=user_id, user_id=user_id)
    user_nickname = data.user.first_name
    if data.user.last_name:
        user_nickname = user_nickname + f" {data.user.last_name}"

    username = data.user.username

    await connect.request(
        "INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?)", (
            user_id,
            ConfigValues.games_amount,
            0,
            user_nickname,
            username,
            None, None))

    await __download_user_avatar(user_id)


@sync_to_async()
def get_ip(request):
    return get_client_ip(request)


@sync_to_async()
def get_session_key(request: HttpRequest):
    return request.COOKIES.get('sessionid')
