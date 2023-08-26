from django.http import HttpRequest
from django.shortcuts import render
from asgiref.sync import sync_to_async

from web_django.authorization.core import get_session_key
from core import get
from Game import games


async def index(request: HttpRequest, *args, **kwargs):

	#try:

		#game_object = get(games, '', tag=kwargs['tag'])
		#assert game_object

		#session_key = await get_session_key(request)

		#if get(game_object.players, '', session_id=session_key):
			#return await player_mode(request)

		#return await spectator_mode(request)

	#except AssertionError:
		#pass  # Во избежание флуда в консоли

	return render(request, 'chessboards/game.html', {"board_tag": kwargs['tag']})


@sync_to_async()
def player_mode(request: HttpRequest):
	return render(request, 'chessboards/game.html')


@sync_to_async()
def spectator_mode(request: HttpRequest):
	return render(request, 'chessboards/game_spectator.html')


def board_view(request: HttpRequest, *args, **kwargs):
	return render(request, 'chessboards/chess.html')



