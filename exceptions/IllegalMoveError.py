from config.ConfigValues import ConfigValues
from exceptions.BaseError import BaseError


class IllegalMoveError(BaseError):
	def __init__(self):
		super().__init__(ConfigValues.illegal_move_error)
