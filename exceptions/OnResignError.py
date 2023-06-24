from config.ConfigValues import ConfigValues
from exceptions.BaseError import BaseError


class OnResignError(BaseError):
	def __init__(self, color: str):
		super().__init__(ConfigValues.on_resign.replace('{color}', color))
