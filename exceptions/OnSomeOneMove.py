from config.ConfigValues import ConfigValues
from exceptions.BaseError import BaseError


class OnSomeOneMove(BaseError):
	def __init__(self):
		super().__init__(ConfigValues.on_someone_move)
			