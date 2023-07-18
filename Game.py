from asyncio import TaskGroup
from uuid import uuid4
from time import time

import chess

from User import User
from exceptions.MateError import MateError
from exceptions.DrawError import DrawError


class Game:
	"""Класс отвечающий за игру"""

	def __init__(self, users_ids: tuple):
		self.board: chess.Board = chess.Board()
		self.player_1: User = User(users_ids[0], True, self)
		self.player_2: User = User(users_ids[1], False, self)
		self.players: list = []
		self.start_time = time()
		self.tag = uuid4()

		games.append(self)

	async def move(self, text_move):
		""":raise BaseError если на доске ситуация приводящая к концу игры либо противоречащая её продолжению"""

		self.board.push_san(text_move)
		self.checkmate()
		self.check_stalemate()

	def checkmate(self):
		""":raise MateError если есть на доске мат"""

		if self.board.is_checkmate():
			raise MateError(self.get_winner().color_text)

	def check_stalemate(self):
		""":raise DrawError если на доске пат"""

		if self.board.is_stalemate():
			raise DrawError()

	def get_winner(self) -> User:
		""":return User - object"""

		return self.player_1 if not self.board.turn else self.player_2

	async def start_timers_game(self):
		"""actions before start game"""

		async with TaskGroup as tasks:
			for user in self.players:
				tasks.create_task(user.fill_attributes())
				tasks.create_task(user.start_timer())

	async def on_end_game(self):
		"""Коро хендлер срабатывающий после окончания игры"""

		self.player_1.stop_timer()
		self.player_2.stop_timer()

		await self.player_1.remove_games()
		await self.player_2.remove_games()

		await self.get_winner().give_points()


games = []
