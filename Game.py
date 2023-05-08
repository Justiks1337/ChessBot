from User import User
import chess
from DatabaseAssistant import request


class Game:
	"""Класс отвечающий за игру"""
	def __init__(self, users_ids: tuple):
		self.board: chess.Board = chess.Board()
		self.player_1: User = User(users_ids[0], True)
		self.player_2: User = User(users_ids[1], False)
		self.turn: bool = self.board.turn

	async def move(self, start_cell: str, end_cell: str):
		""":raise AssertionError если возникает какая либо ошибка."""
		try:
			self.board.push_san("".join([start_cell, end_cell]))
			self.checkmate()
			self.check_stalemate()
		except chess.IllegalMoveError:
			assert False, "Такой ход не возможен!"

	def checkmate(self):
		""":raise AssertionError если есть на доске мат"""
		assert not self.board.is_checkmate(), f"Мат! Победил {self.get_winner_color()} цвет!"

	def check_stalemate(self):
		""":raise AssertionError если на доске пат"""
		assert not self.board.is_stalemate(), "Игра окончена! Ничья, оба участника остаются без баллов..."

	def get_winner_color(self) -> str:
		""":return Возвращает цвет победителя (При мате)"""
		return "белый" if self.turn else "чёрный"

	def get_winner(self) -> User:
		""":return User - object """
		return self.player_1 if not self.player_1.color is self.turn else self.player_2

	@staticmethod
	async def give_points(user: User):
		"""Добавляет баллы в базу данных"""
		await request("UPDATE users SET points = points + 1 WHERE user_id = ?", (user.telegram_id, ))

	async def on_end_game(self):
		"""Коро хендлер срабатывающий после окончания игры"""
		await self.give_points(self.get_winner())
