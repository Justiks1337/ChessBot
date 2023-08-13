from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.renderers import JSONRenderer
from adrf.decorators import api_view

from .serializers import (StartGameSerializer,
                          NewAuthorizeTokenSerializer,
                          DeleteAuthorizeTokenSerializer,
                          AuthorizeAttemptSerializer,
                          ChessboardMoveSerializer,
                          ChessboardDrawSerializer,
                          ChessboardGiveUpSerializer)

from .responses import (StartGameResponse,
                        NewAuthorizeTokenResponse,
                        DeleteAuthorizeTokenResponse,
                        AuthorizeAttemptResponse,
                        ChessboardMoveResponse,
                        ChessboardDrawResponse,
                        ChessboardGiveUpResponse)

from database_tools.Connection import connect
from .authorization import authorization
from Authorization import main_authorization
from web_django.authorization.core import get_session_key
from exceptions.DuplicateAuthorizationTokenError import DuplicateAuthorizationTokenError
from exceptions.UnsuccessfulAuthorization import UnsuccessfulAuthorization
from exceptions.OnSomeoneMoveError import OnSomeoneMoveError
from exceptions.IllegalMoveError import IllegalMoveError
from web_django.chessboards.games_management import game_start
from Game import games
from core import get
from User import User
from config.ConfigValues import ConfigValues

# Create your views here.


class StartGameView(APIView):
    @authorization
    def post(self, request: Request):

        first_user_id = request.query_params.get('first_user_id')
        second_user_id = request.query_params.get('second_user_id')

        token = game_start(first_user_id, second_user_id)

        return Response(StartGameSerializer(StartGameResponse(token)).data)


class NewAuthorizeTokenView(APIView):
    @authorization
    def post(self, request: Request):

        user_id = request.query_params.get("user_id")

        try:

            token = main_authorization.new_token(user_id)

            return Response(NewAuthorizeTokenSerializer(NewAuthorizeTokenResponse(True, token)).data)

        except DuplicateAuthorizationTokenError:
            return Response(NewAuthorizeTokenSerializer(NewAuthorizeTokenResponse(False, '')).data)


class DeleteAuthorizeTokenView(APIView):
    @authorization
    def post(self, request: Request):

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


@api_view(['POST'])
async def chessboard_move(request: Request):

    player: User = get(games, "players", session_id=request.COOKIES.get('sessionid'))

    if not player:
        return Response(JSONRenderer().render(ChessboardMoveSerializer(ChessboardMoveResponse(
            False,
            message="сурс проекта: https://github.com/Justiks228/ChessBot, чекни его. Попытка была хорошая")).data))

    start_cell = request.query_params.get('start_cell')
    end_cell = request.query_params.get('end_cell')

    try:
        player.move(start_cell, end_cell)
        response = ChessboardMoveResponse(True, board=player.own_object.board.fen(), time=player.timer.time)

    except OnSomeoneMoveError:
        response = ChessboardMoveResponse(False, message=ConfigValues.on_someone_move)

    except IllegalMoveError:
        response = ChessboardMoveResponse(False, message=ConfigValues.illegal_move_error)

    return Response(JSONRenderer().render(ChessboardMoveSerializer(response).data))


@api_view(['POST'])
async def chessboard_draw(request: Request):

    player: User = get(games, "players", session_id=request.COOKIES.get('sessionid'))

    if not player:
        return Response(JSONRenderer().render(ChessboardDrawSerializer(ChessboardDrawResponse(False)).data))

    await player.draw()
    return Response(JSONRenderer().render(ChessboardDrawSerializer(ChessboardDrawResponse(True)).data))


@api_view(['POST'])
async def chessboard_give_up(request: Request):
    player: User = get(games, "players", session_id=request.COOKIES.get('sessionid'))

    if not player:
        return Response(JSONRenderer().render(ChessboardGiveUpSerializer(ChessboardGiveUpResponse(False)).data))

    await player.give_up()
    return Response(JSONRenderer().render(ChessboardGiveUpSerializer(ChessboardGiveUpResponse(True)).data))
