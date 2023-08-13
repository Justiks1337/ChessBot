from config.ConfigValues import ConfigValues
from asyncio import Event, wait_for, TimeoutError
from time import time as _time


class Timer:
	"""class Timer"""

	def __init__(
			self,
			own_object,
			time: int = ConfigValues.game_time
	):
		self.__event = Event()

		self.own_object = own_object
		self.time = time

	async def __wait_move(self):
		"""wait move"""
		last_move_time = _time()

		await self.__event.wait()

		self.time = self.time - (_time() - last_move_time)
		self.__event.clear()

	async def start_timer(self):
		"""Start the timer"""
		while self.time > 0:

			await self.__event.wait()
			self.__event.clear()

			try:
				await wait_for(self.__wait_move(), timeout=self.time)
			except TimeoutError:
				await self.own_object.own_object.on_end_timer(self.own_object)

	def flip_the_timer(self):
		"""Меняет положение таймера (активный/деактивный)"""

		self.__event.set()

	def stop_the_timer(self):
		"""Stop the timer"""

		self.time = 0  # timer loop has condition self.time > 0. I'm killing timer loop by changing the condition
		self.flip_the_timer()  # back to loop start and kill timer loop
		self.flip_the_timer()  # if timer in activity position
