import os

from django.shortcuts import render
from asgiref.sync import sync_to_async
import jwt

from api.utils import in_database
from chessboards.models import UserModel


async def index(request):
    token = request.GET.get('token')

    try:
        decoded_token = jwt.decode(token, os.getenv("SERVER_AUTHKEY"), algorithms=["HS256"])

    except (jwt.ExpiredSignatureError, jwt.DecodeError, jwt.InvalidTokenError):
        return render(request, 'error_page/index.html', {"error": "Токен не валидный или истек", "error_code": "401"})

    user_id = decoded_token["user_id"]
    username = decoded_token["username"]
    nickname = decoded_token["nickname"]

    await sync_to_async(request.session.update)({"user_id": user_id})

    if not await in_database(user_id):
        user = await UserModel.objects.acreate(user_id=user_id, points=0, username=username, nickname=nickname)
        await user.asave()

    return render(request, "authorization/success_authorization.html")
