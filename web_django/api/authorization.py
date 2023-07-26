from rest_framework.response import Response
from rest_framework.request import Request

from config.ConfigValues import ConfigValues


def authorization(func):
    def wrapper(self, request: Request):
        try:
            if request.META.get("HTTP_AUTHORIZATION") == ConfigValues.server_authkey:
                return func(self, request)
            return Response({'Неверный ключ авторизации!'})

        except KeyError:
            return Response({'Неверный ключ авторизации!'})
    return wrapper
