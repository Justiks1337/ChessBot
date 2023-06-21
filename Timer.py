from time import sleep
from exceptions.BaseErrors import ChessError
from config.ConfigValues import ConfigValues
from threading import Thread


class Timer:
	"""class Timer"""

	def __init__(self, color: bool):
		self.color = lambda x: "белых" if color else "чёрных"
		self.time = int(ConfigValues.game_time)
		self.ticking = color
		self.thread = Thread(target=self.timer)
		self.thread.start()

	def timer(self):
		"""Отсчёт времени"""

		if self.ticking:

			sleep(1)
			self.time = self.time - 1
			print(self.time)

			try:
				assert self.time
			except AssertionError:
				raise ChessError(ConfigValues.on_end_time.replace('{color}', self.color))

			self.timer()  # recursion

		return

	def flip_the_timer(self):
		"""Меняет положение таймера (активный/деактивный)"""

		self.ticking = not self.ticking

		if self.ticking:
			Thread(target=self.timer).start()
			return
		self.thread.join()


Timer(True)
Timer(True)
