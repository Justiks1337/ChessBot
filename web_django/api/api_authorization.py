from rest_framework.response import Response
from rest_framework.request import Request

from config.Config import Config


def authorization(func):
    async def wrapper(request: Request):
        try:
            if request.META.get("HTTP_AUTHORIZATION") == Config.server_authkey:
                return await func(request)

            return Response({'Неверный ключ авторизации!'})

        except KeyError:

            return Response({'Неверный ключ авторизации!'})
    return wrapper
