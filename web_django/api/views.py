from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpRequest

from .serializers import StartGameSerializer, NewAuthorizeTokenSerializer, DeleteAuthorizeTokenSerializer
from .responses import StartGameResponse, NewAuthorizeTokenResponse, DeleteAuthorizeTokenResponse
from .authorization import authorization
from Authorization import main_authorization
from exceptions.DuplicateAuthorizationTokenError import DuplicateAuthorizationTokenError
from chessboards.games_management import game_start

# Create your views here.


class StartGameView(APIView):
    @authorization
    def post(self, request: HttpRequest):

        first_user_id = request.POST.get('first_user_id')
        second_user_id = request.POST.get('second_user_id')

        token = game_start(first_user_id, second_user_id)

        return Response(StartGameSerializer(StartGameResponse(token)).data)


class NewAuthorizeTokenView(APIView):
    @authorization
    def post(self, request: HttpRequest):

        try:
            token = main_authorization.new_token(request.POST.get("user_id"))
            return Response(NewAuthorizeTokenSerializer(NewAuthorizeTokenResponse(True, token)).data)

        except DuplicateAuthorizationTokenError:
            return Response(NewAuthorizeTokenSerializer(NewAuthorizeTokenResponse(False, '')).data)


class DeleteAuthorizeTokenView(APIView):
    @authorization
    def post(self, request: HttpRequest):

        user_id = request.POST.get('user_id')

        try:
            main_authorization.remove_token(user_id)
            return Response(DeleteAuthorizeTokenSerializer(DeleteAuthorizeTokenResponse(True)).data)

        except KeyError:
            return Response(DeleteAuthorizeTokenSerializer(DeleteAuthorizeTokenResponse(False)).data)
