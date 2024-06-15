import datetime
import os
from asyncio import get_running_loop
from time import time

from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.renderers import JSONRenderer
from rest_framework.generics import RetrieveAPIView
from rest_framework.serializers import ModelSerializer
from adrf.decorators import api_view
from api.utils import in_database
from asgiref import sync
import jwt

from .serializers import (
    StartGameSerializer,
    CheckInGameSerializer,
    NewAuthorizeTokenSerializer,
    AuthorizeAttemptSerializer)

from .responses import (
    StartGameResponse,
    CheckInGameResponse,
    NewAuthorizeTokenResponse,
    AuthorizeAttemptResponse)

from api.utils import authorization

from chessboards.chess_core.core import get
from chessboards.chess_core.Game import games, Game
from chessboards.models import UserModel


@api_view(['POST'])
@authorization
async def start_game(request: Request):
    first_user_id, second_user_id = map(int, await sync.sync_to_async(request.data.get)('players'))

    game = Game((first_user_id, second_user_id))

    get_running_loop().create_task(game.start_timers_game())

    return Response(StartGameSerializer(StartGameResponse(game.tag)).data)


@api_view(['POST'])
@authorization
async def check_in_game(request: Request):
    user_id = request.query_params.get('user_id')

    user = await get(games, 'players', _user_id=user_id)

    if user:
        return Response(CheckInGameSerializer(CheckInGameResponse(True)).data)

    return Response(CheckInGameSerializer(CheckInGameResponse(False)).data)


@api_view(['POST'])
@authorization
async def new_authorize_token(request: Request):
    user_id = await sync.sync_to_async(request.query_params.get)("user_id")
    username = await sync.sync_to_async(request.query_params.get)("username")
    nickname = await sync.sync_to_async(request.query_params.get)("nickname")

    token = jwt.encode({"user_id": user_id,
                        "username": username,
                        "nickname": nickname,
                        "exp": time() + int(os.getenv("JWT_LIVETIME"))},
                       os.getenv("SERVER_AUTHKEY"))

    return Response(NewAuthorizeTokenSerializer(NewAuthorizeTokenResponse(True, token)).data)


@api_view(['POST'])
async def authorization_attempt(request: Request):
    token = request.query_params.get('token')

    decoded_token = jwt.decode(token, os.getenv("SERVER_AUTHKEY"), algorithms=["HS256"])

    if not decoded_token.get("user_id"):
        return Response(JSONRenderer().render(AuthorizeAttemptSerializer(AuthorizeAttemptResponse(False, message="Invalid token")).data))

    if decoded_token.get("created_at") + 300 < time():
        return Response(JSONRenderer().render(AuthorizeAttemptSerializer(AuthorizeAttemptResponse(False, message="Token expired")).data))

    user_id = decoded_token["user_id"]
    username = decoded_token["username"]
    nickname = decoded_token["nickname"]

    request.session["user_id"] = user_id

    if not await in_database(user_id):
        user = await UserModel.objects.acreate(user_id=user_id, points=0, username=username, nickname=nickname)
        await user.asave()

    return Response(JSONRenderer().render(AuthorizeAttemptSerializer(AuthorizeAttemptResponse(True)).data))


@api_view(['POST'])
async def check_timer(request: Request):
    game_tag = request.query_params.get("tag")

    game: Game = await get(games, '', tag=game_tag)

    if not game:
        return Response({"status": 200})

    player = game.get_turn_player()

    if time() - player.timer.last_flip > player.timer.time:
        await game.on_end_timer(player)

    return Response({'status': 200})


@api_view(['POST'])
@authorization
async def download_avatar(request: Request):
    file = request.FILES["file"]
    file_name = request.query_params.get("file_name")
    with open(os.path.join(os.getenv("PATH_TO_AVATARS"), file_name), "wb") as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    return Response({"status": 200})


@api_view(['GET'])
@authorization
async def in_database_api(request: Request):
    user_id = request.query_params.get("user_id")

    if await in_database(user_id):
        return Response({"in_database": True})

    return Response({"in_database": False})


@api_view(['GET'])
@authorization
async def dashboard(request: Request):

    count = int(request.query_params.get("count"))
    if not count:
        users = UserModel.objects.all().order_by("-points")
    else:
        users = UserModel.objects.all().order_by("-points")[:count]

    json = [{"user_id": user.user_id, "points": user.points, "nickname": user.nickname} async for user in users]

    return Response(json)


class UserInfo(RetrieveAPIView):
    class Serializer(ModelSerializer):
        class Meta:
            model = UserModel
            fields = ["points"]

    queryset = UserModel.objects.all()
    serializer_class = Serializer
    lookup_field = "user_id"
