from django.http import HttpRequest
from django.shortcuts import render
from asgiref.sync import sync_to_async

from web_django.authorization.core import get_session_key
from core import get
from Game import games


async def game_view(request: HttpRequest, **kwargs):

	try:

		game_object = get(games, '', tag=kwargs['tag'])
		assert game_object

		kwargs["game"] = game_object

		session_key = await get_session_key(request)

		if get(game_object.players, '', session_id=session_key):
			return await game_player_mode(request, **kwargs)

		return await game_spectator_mode(request, **kwargs)

	except AssertionError:
		return render(request, 'error_page/index.html', {'error_number': '404'})


@sync_to_async()
def game_player_mode(request: HttpRequest, **kwargs):

	game = kwargs["game"]
	user = get(games, 'players', session_id=request.COOKIES.get('sessionid'))

	return render(request, 'chessboards/game.html', {
		'board_tag': kwargs['tag'],
		'user_id': user.user_id,
		'board_fen': game.board.board_fen(),
		'first_player_nickname': game.player_1.nickname,
		'second_player_nickname': game.player_2.nickname,
		'first_player_avatar': game.player_1.avatar_path,
		'second_player_avatar': game.player_2.avatar_path,
		'first_player_time': round(game.player_1.timer.time),
		'second_player_time': round(game.player_2.timer.time),
		'draw_offer': user.draw_offer,
		'color': user.color,
		'turn': game.board.turn})


@sync_to_async()
def game_spectator_mode(request: HttpRequest, **kwargs):
	
	game = kwargs["game"]

	return render(request, 'chessboards/game_spectator.html', {
		'board_tag': kwargs['tag'],
		'board_fen': game.board.board_fen(),
		'first_player_nickname': game.player_1.nickname,
		'second_player_nickname': game.player_2.nickname,
		'first_player_avatar': game.player_1.avatar_path,
		'second_player_avatar': game.player_2.avatar_path,
		'first_player_time': round(game.player_1.timer.time),
		'second_player_time': round(game.player_2.timer.time)})
