from config.ConfigValues import ConfigValues
from asyncio import Event, wait_for, TimeoutError
from time import time as _time
from core import on_end_time_error


class Timer:
	"""class Timer"""

	def __init__(
			self,
			on_end_time_func=on_end_time_error,
			time: int = int(ConfigValues.game_time)
	):
		self.__function = on_end_time_func
		self.__initialize = False

		self.time = time
		self.event = Event()

	async def __wait_move(self):
		"""wait move"""
		last_move_time = _time()

		await self.event.wait()

		self.time = self.time - (_time() - last_move_time)
		self.event.clear()

	async def start_timer(self):
		"""Start the timer"""
		while self.time > 0:
			if self.__initialize:
				await self.event.wait()
				self.event.clear()
			else:
				self.__initialize = True

			try:
				await wait_for(self.__wait_move(), timeout=self.time)
			except TimeoutError:
				self.__function()

	async def flip_the_timer(self):
		"""Меняет положение таймера (активный/деактивный)"""

		self.event.set()

	async def stop_the_timer(self):
		"""Stop the timer"""

		self.time = 0  # timer loop has condition self.time > 0. I'm killing timer loop by changing the condition
		await self.flip_the_timer()  # back to loop start and kill timer loop
