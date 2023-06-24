from config.ConfigValues import ConfigValues
from exceptions.BaseError import BaseError


class IllegalMoveError:
	def __init__(self):
		raise BaseError(ConfigValues.illegal_move_error)
