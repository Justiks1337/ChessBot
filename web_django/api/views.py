from asyncio import create_task, get_running_loop

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

from .responses import (StartGameResponse,
                        CheckInGameResponse,
                        NewAuthorizeTokenResponse,
                        DeleteAuthorizeTokenResponse,
                        AuthorizeAttemptResponse)

from database_tools.Connection import connect
from .authorization import authorization
from Authorization import main_authorization
from web_django.authorization.core import get_session_key
from exceptions.DuplicateAuthorizationTokenError import DuplicateAuthorizationTokenError
from exceptions.UnsuccessfulAuthorization import UnsuccessfulAuthorization
from core import get
from Game import games


@api_view(['POST'])
@authorization
async def check_in_game(request: Request):

    user_id = request.query_params.get('user_id')

    user = get(games, 'players', user_id=user_id)

    if user:
        return Response(CheckInGameSerializer(CheckInGameResponse(True)).data)

    return Response(CheckInGameSerializer(CheckInGameResponse(False)).data)


@api_view(['POST'])
@authorization
async def new_authorize_token(request: Request):

    user_id = request.query_params.get("user_id")

    try:

        token = main_authorization.new_token(user_id)

        return Response(NewAuthorizeTokenSerializer(NewAuthorizeTokenResponse(True, token)).data)

    except DuplicateAuthorizationTokenError:
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

    try:

        user_id = await main_authorization.authorization(token)

        session_key = await get_session_key(request)

        await connect.request("UPDATE users SET session_id = ? WHERE user_id = ?", (session_key, user_id))

        return Response(JSONRenderer().render(AuthorizeAttemptSerializer(AuthorizeAttemptResponse(True)).data))

    except UnsuccessfulAuthorization:
        return Response(JSONRenderer().render(AuthorizeAttemptSerializer(AuthorizeAttemptResponse(False)).data))
