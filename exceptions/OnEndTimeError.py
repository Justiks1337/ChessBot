from config.ConfigValues import ConfigValues
from exceptions.BaseError import BaseError


class OnEndTimeError(BaseError):
	def __init__(self, color: str):
		raise BaseError(ConfigValues.on_end_time.replace('{color}', color))
