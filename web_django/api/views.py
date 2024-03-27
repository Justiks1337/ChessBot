from asyncio import get_running_loop
from time import time

from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.renderers import JSONRenderer
from adrf.decorators import api_view

from .serializers import (
    StartGameSerializer,
    CheckInGameSerializer,
    NewAuthorizeTokenSerializer,
    DeleteAuthorizeTokenSerializer,
    AuthorizeAttemptSerializer)

from .responses import (
    StartGameResponse,
    CheckInGameResponse,
    NewAuthorizeTokenResponse,
    DeleteAuthorizeTokenResponse,
    AuthorizeAttemptResponse)

from database_tools.Connection import connect
from .authorization import authorization
from web_django.api.Authorization import main_authorization
from web_django.authorization.core import get_session_key, get_ip
from chess_core.core import get
from chess_core.Game import games, Game


@api_view(['POST'])
@authorization
async def start_game(request: Request):

    first_user_id, second_user_id = map(int, request.META.get('HTTP_PLAYERS'))

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
    user_id = request.query_params.get("user_id")

    token = main_authorization.new_token(user_id)

    if token:
        return Response(NewAuthorizeTokenSerializer(NewAuthorizeTokenResponse(True, token)).data)

    return Response(NewAuthorizeTokenSerializer(NewAuthorizeTokenResponse(False, '')).data)


@authorization
@api_view(['POST'])
async def delete_authorize_token(request: Request):
    user_id = request.query_params.get('user_id')
    try:
        main_authorization.remove_token(user_id)
        return Response(DeleteAuthorizeTokenSerializer(DeleteAuthorizeTokenResponse(True)).data)

    except KeyError:
        return Response(DeleteAuthorizeTokenSerializer(DeleteAuthorizeTokenResponse(False)).data)


@api_view(['POST'])
async def authorization_attempt(request: Request):
    token = request.query_params.get('token')
    ip = await get_ip(request)

    user_id = await main_authorization.authorization(token)

    if user_id:
        session_key = await get_session_key(request)

        await connect.request("UPDATE users SET session_id = ?, ip_address = ? WHERE user_id = ?", (
            session_key,
            ip[0],
            user_id))

        user = await get(games, 'players', _user_id=user_id)

        if user:
            user.session_id = session_key

        return Response(JSONRenderer().render(AuthorizeAttemptSerializer(AuthorizeAttemptResponse(True)).data))

    return Response(JSONRenderer().render(AuthorizeAttemptSerializer(AuthorizeAttemptResponse(False)).data))


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
