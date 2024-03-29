from sqlite3 import IntegrityError

from aiogram import Bot
from asgiref.sync import sync_to_async
from django.http import HttpRequest
from ipware import get_client_ip

from chessboards.models import UserModel
from config.Config import Config


bot = Bot(Config.telegram_token)


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
        await bot.download_file(file.file_path, file_destination)


def get_file_name(file_path: str) -> str:
    return file_path[-file_path[::-1].index('/'):]


def get_file_format(file_name: str) -> str:
    return file_name[file_name.index('.'):]


def get_destination(user_id: int, file_name) -> str:

    file_format = get_file_format(file_name)

    file_destination = Config.path_to_avatars + str(user_id) + file_format

    return file_destination


async def new_data(user_id: int):
    data = await bot.get_chat_member(chat_id=user_id, user_id=user_id)
    user_nickname = data.user.first_name
    if data.user.last_name:
        user_nickname = user_nickname + f" {data.user.last_name}"

    username = data.user.username

    user = UserModel(
        user_id=user_id,
        games=Config.games_amount,
        points=0,
        nickname=user_nickname,
        username=username,
        session_id=None,
        ip_address=None)

    await user.asave()

    await __download_user_avatar(user_id)


@sync_to_async()
def get_ip(request):
    return get_client_ip(request)


@sync_to_async()
def get_session_key(request: HttpRequest):
    return request.COOKIES.get('sessionid')
