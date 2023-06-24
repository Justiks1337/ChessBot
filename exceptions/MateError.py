from config.ConfigValues import ConfigValues
from exceptions.BaseError import BaseError


class MateError(BaseError):
	def __init__(self, color: str):
		super().__init__(
			ConfigValues.on_mate_message.replace('{color}', color)
		)
