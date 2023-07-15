from rest_framework.response import Response
from django.http import HttpResponse

from config.ConfigValues import ConfigValues


def authorization(func):
    def wrapper(self, request: HttpResponse):
        try:
            if request.headers['Authorization'] == ConfigValues.server_authkey:
                return func(self, request)
            return Response({'Неверный ключ авторизации!'})

        except KeyError:
            return Response({'Неверный ключ авторизации!'})
    return wrapper
