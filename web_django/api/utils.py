import os

from rest_framework.response import Response
from rest_framework.request import Request

<<<<<<<< HEAD:web_django/api/utils.py
from chessboards.models import UserModel


async def in_database(user_id: int) -> bool:

    try:
        await UserModel.objects.aget(user_id=user_id)
        return True

    except UserModel.DoesNotExist:
        return False

========
>>>>>>>> refs/remotes/origin/main:web_django/api/api_authorization.py

def authorization(func):
    async def wrapper(request: Request):
        try:
            if request.META.get("HTTP_AUTHORIZATION") == os.getenv("SERVER_AUTHKEY"):
                return await func(request)

            return Response({'Неверный ключ авторизации!'})

        except KeyError:

            return Response({'Неверный ключ авторизации!'})
    return wrapper
