from config.ConfigValues import ConfigValues
from exceptions.BaseError import BaseError


class OnEndTimeError(BaseError):
	def __init__(self, color: str):
		super().__init__(
			ConfigValues.on_end_time.replace('{color}', color)
		)
