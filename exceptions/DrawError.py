from config.ConfigValues import ConfigValues
from exceptions.BaseError import BaseError


class DrawError(BaseError):
	def __init__(self):
		super().__init__(
			ConfigValues.on_draw_message
		)
