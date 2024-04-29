import os
import asyncio
from uuid import uuid4
from time import time
from typing import Optional

import chess
from channels.consumer import get_channel_layer

from chessboards.chess_core.User import User
from chessboards.models import GamesModel


class Game:
	"""Класс отвечающий за игру"""

	def __init__(self, users_ids: tuple):
		self.board: chess.Board = chess.Board()
		self.players: list = []
		self.player_1: User = User(users_ids[0], True, self)
		self.player_2: User = User(users_ids[1], False, self)
		self._started_at = time()
		self.tag = str(uuid4())
		self.game_end: bool = False

		games.append(self)

	@property
	def started_at(self):
		return round(self._started_at)

	async def move(self, text_move):
		""":raise BaseError если на доске ситуация приводящая к концу игры либо противоречащая её продолжению"""

		turn_player = self.get_turn_player()

		try:

			self.board.push_san(text_move)
		except chess.IllegalMoveError as error:
			if "missing promotion piece type" in error.args[0]:
				self.board.push_san(f"{text_move}q")
			else:
				raise chess.IllegalMoveError()

		asyncio.get_running_loop().create_task(self.get_turn_player().start_timer(), name=self.tag)

		await turn_player.timer.flip_the_timer()

		await channel_layer.group_send(
			self.tag,
			{
				"type": "update_board",
				"board": self.board.board_fen(),
				"first_user_time": 	self.player_1.timer.time,
				"second_user_time": self.player_2.timer.time
			}
		)

		await self.move_checks()

		return self.board.board_fen()

	async def checkmate(self):
		""":raise MateError если есть на доске мат"""

		if self.board.is_checkmate():
			winner = self.get_winner()
			await self.on_win(winner, os.getenv("ON_MATE_MESSAGE").replace('{color}', winner.color_text))

	async def check_stalemate(self):
		""":raise DrawError если на доске пат"""

		if self.board.is_stalemate():
			await self.on_end_game(os.getenv("ON_STALEMATE_MESSAGE"))

	async def on_check(self):
		if self.board.is_check():
			await channel_layer.group_send(
				self.tag,
				{
					'type': 'on_check',
					'recipient': self.get_turn_player().user_id
				}
			)

	async def move_checks(self):
		await self.checkmate()
		await self.check_stalemate()
		await self.on_check()

	def get_winner(self) -> User:
		""":return User - object"""

		return self.player_1 if not self.board.turn else self.player_2

	def get_turn_player(self):
		""":return User object"""

		return self.player_1 if self.player_1.color is self.board.turn else self.player_2

	async def start_timers_game(self):
		"""actions before start game"""

		for player in self.players:
			asyncio.get_running_loop().create_task(player.fill_attributes())

		await asyncio.sleep(int(os.getenv("PREPARE_TIME")))

		asyncio.get_running_loop().create_task(self.get_turn_player().start_timer(), name=self.tag)

	async def on_end_game(self, message):
		"""Коро хендлер срабатывающий после окончания игры"""

		if self.game_end:
			return

		self.game_end = True

		self.delete_timers()

		await channel_layer.group_send(
			self.tag,
			{
				'type': "end_game_event",
				'message': message
			})

		await self.player_1.remove_games()
		await self.player_2.remove_games()

		games.remove(self)
		del self

	def delete_timers(self):
		for task in asyncio.all_tasks(asyncio.get_running_loop()):
			if task.get_name() == self.tag:
				task.cancel()

	async def on_win(self, winner: User, message: str):
		await self.on_end_game(message)
		await winner.give_points()
		await self.add_to_game_registry(winner)

	async def on_draw(self):
		await self.add_to_game_registry(None)

	async def add_to_game_registry(self, winner: Optional[User]):

		game = GamesModel(
				first_player=self.player_1.model_user,
				second_player=self.player_2.model_user,
				winner=winner.model_user
		)
		await game.asave()

	async def on_draw_offer(self):
		for player in self.players:
			if not player.draw_offer:

				await channel_layer.group_send(
					self.tag,
					{
						'type': "draw_offer_event",
						'recipient': player.user_id
					}
				)
				return

		await self.on_end_game(os.getenv("ON_DRAW_MESSAGE"))

	async def on_give_up(self, user_id: int):
		for player in self.players:
			if player.user_id != user_id:
				await self.on_win(player, os.getenv("ON_RESIGN").replace('{color}', player.color_text))

	async def on_end_timer(self, loser: User):

		if self.game_end:
			return

		# noinspection PyTypeChecker

		await self.on_win((lambda player: self.player_1 if player == self.player_2 else self.player_2)(loser), os.getenv("ON_END_TIME").replace('{color}', loser.color_text))

	def get_legal_moves(self, cell: str) -> list:

		""":return legal moves for piece on cell"""

		return [str(move)[2:] for move in self.board.legal_moves if str(move)[:2] == cell]


channel_layer = get_channel_layer("default")
games = []
