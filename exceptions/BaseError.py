from typing import Optional


class BaseError(Exception):
	"""Класс ошибки вызываемый вместо AssertionError"""
	def __init__(
			self,
			message: str,
			session=None,
			page: Optional[str] = None):

		self.message = message
