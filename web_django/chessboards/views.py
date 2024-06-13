import os
from time import time

from django.http import HttpRequest
from django.shortcuts import render
from asgiref.sync import sync_to_async

from chessboards.chess_core.core import get
from chessboards.chess_core.Game import games


async def game_view(request: HttpRequest, **kwargs):

	game_object = await get(games, '', tag=kwargs['tag'])
	user_id = await sync_to_async(request.session.get)("user_id")

	if not game_object or not user_id:
		return await sync_to_async(render)(request, 'error_page/index.html', {'error_number': '404'})

	user_id = int(user_id)

	user = await get(game_object.players, '', user_id=user_id)

	kwargs["game"] = game_object
	kwargs["user"] = user

	await game_object.get_turn_player().timer.update_timer()

	if user:
		return await game_player_mode(request, **kwargs)

	return await game_spectator_mode(request, **kwargs)


@sync_to_async()
def game_player_mode(request: HttpRequest, **kwargs):

	game = kwargs["game"]
	user = kwargs["user"]

	return render(request, 'chessboards/game.html', {
		'prepare_time': int(os.getenv("PREPARE_TIME")) - round(time() - game.started_at),
		'board_tag': kwargs['tag'],
		'user_id': user.user_id,
		'board_fen': game.board.board_fen(),
		'first_player_nickname': game.player_1.nickname,
		'second_player_nickname': game.player_2.nickname,
		'first_player_avatar': game.player_1.avatar_path,
		'second_player_avatar': game.player_2.avatar_path,
		'first_player_time': game.player_1.timer.time,
		'second_player_time': game.player_2.timer.time,
		'draw_offer': user.draw_offer,
		'color': user.color,
		'turn': game.board.turn})


@sync_to_async()
def game_spectator_mode(request: HttpRequest, **kwargs):
	
	game = kwargs["game"]

	return render(request, 'chessboards/game_spectator.html', {
		'prepare_time': int(os.getenv('PREPARE_TIME')) - round(time() - game.started_at),
		'board_tag': kwargs['tag'],
		'board_fen': game.board.board_fen(),
		'first_player_nickname': game.player_1.nickname,
		'second_player_nickname': game.player_2.nickname,
		'first_player_avatar': game.player_1.avatar_path,
		'second_player_avatar': game.player_2.avatar_path,
		'first_player_time': game.player_1.timer.time,
		'second_player_time': game.player_2.timer.time,
		'turn': game.board.turn})
