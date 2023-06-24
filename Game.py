import gc

from User import User
import chess
from exceptions.MateError import MateError
from exceptions.DrawError import DrawError
from asyncio import create_task
from uuid import uuid4


class Game:
	"""Класс отвечающий за игру"""

	def __init__(self, users_ids: tuple):
		self.board: chess.Board = chess.Board()
		self.player_1: User = User(users_ids[0], True, self)
		self.player_2: User = User(users_ids[1], False, self)
		self.tag = uuid4()

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

	async def prepare_to_game(self):
		"""actions before start game"""

		first_timer = create_task(self.player_1.start_timer())  # first_timer - invisible reference to timer, for GC
		second_timer = create_task(self.player_2.start_timer())  # second_timer - invisible reference to timer, for GC
		self.player_2.timer_continue()

	async def on_end_game(self):
		"""Коро хендлер срабатывающий после окончания игры"""

		self.player_1.stop_timer()
		self.player_2.stop_timer()

		await self.player_1.remove_games()
		await self.player_2.remove_games()

		await self.get_winner().give_points()
