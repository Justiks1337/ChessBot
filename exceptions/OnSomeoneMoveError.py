from config.ConfigValues import ConfigValues
from exceptions.BaseError import BaseError


class OnSomeoneMoveError(BaseError):
	def __init__(self):
		raise BaseError(ConfigValues.on_someone_move)
			