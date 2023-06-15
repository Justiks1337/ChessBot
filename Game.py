from User import User
import chess
from database_tools.Connection import connect
from BaseErrors import ChessError


class Game:
	"""Класс отвечающий за игру"""
	def __init__(self, users_ids: tuple):
		self.board: chess.Board = chess.Board()
		self.player_1: User = User(users_ids[0], True)
		self.player_2: User = User(users_ids[1], False)

	async def move(self, start_cell: str, end_cell: str):
		""":raise ChessError если возникает какая либо ошибка."""

		try:
			self.board.push_san("".join([start_cell, end_cell]))
			self.checkmate()
			self.check_stalemate()

		except chess.IllegalMoveError:
			raise ChessError("Такой ход не возможен!", local=True, color=self.board.turn)

	def checkmate(self):
		""":raise ChessError если есть на доске мат"""
		try:
			assert not self.board.is_checkmate(), f"Мат! Победил {self.get_winner_color()} цвет!"
		except AssertionError:
			raise ChessError(f"Мат! Победил игрок играющий за {self.get_winner_color()} цвет!")

	def check_stalemate(self):
		""":raise ChessError если на доске пат"""
		try:
			assert not self.board.is_stalemate()
		except AssertionError:
			raise ChessError("Игра окончена! Ничья, оба участника остаются без баллов...")

	def get_winner_color(self) -> str:
		""":return Возвращает цвет победителя (При мате)"""
		return "белый" if self.board.turn else "чёрный"

	def get_winner(self) -> User:
		""":return User - object """
		return self.player_1 if not self.player_1.color is self.board.turn else self.player_2

	@staticmethod
	async def give_points(user: User):
		"""Добавляет баллы в базу данных"""
		await connect.request("UPDATE users SET points = points + 1 WHERE user_id = ?", (user.telegram_id, ))

	async def on_end_game(self):
		"""Коро хендлер срабатывающий после окончания игры"""
		await self.give_points(self.get_winner())
