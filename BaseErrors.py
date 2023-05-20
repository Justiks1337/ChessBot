from typing import Optional


class ChessError(Exception):
	"""Класс ошибки вызываемый вместо AssertionError"""
	def __init__(self, message: str, local: Optional[bool] = False, color: Optional[bool] = None):
		self.message = message
		self.local = local
		self.color = color
