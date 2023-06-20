from threading import Thread
from time import sleep
from BaseErrors import ChessError
from config.ConfigValues import ConfigValues


class Timer:
	"""class Timer"""

	def __init__(self, color: bool):
		self.color = lambda x: "белых" if color else "чёрных"
		self.time = ConfigValues.game_time
		self.ticking = color
		self.thread = Thread(target=self.timer)
		self.thread.start()

	def timer(self):
		"""Отсчёт времени"""

		while self.ticking:
			sleep(1)
			self.time = self.time - 1

			try:
				assert self.time
			except AssertionError:
				raise ChessError(ConfigValues.on_end_time.replace('{color}', self.color))
		return

	def flip_the_timer(self):
		"""Меняет положение таймера (активный/деактивный)"""

		self.ticking = not self.ticking

		if self.ticking:
			Thread(target=self.timer).start()
			return
		self.thread.join()
