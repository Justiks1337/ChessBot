from config.ConfigValues import ConfigValues
from asyncio import Event, wait_for, TimeoutError
from time import time as _time


class Timer:
	"""class Timer"""

	def __init__(
			self,
			own_object,
			active_timer: bool,
			time: int = ConfigValues.game_time,
	):
		self.__event = Event()

		self.last_flip = _time()
		self.active_timer = active_timer
		self.own_object = own_object
		self.time = time

	async def __wait_move(self):
		"""wait move"""
		self.last_flip = _time()

		await self.__event.wait()

		self.__event.clear()

	async def start_timer(self):
		"""Start the timer"""
		while self.time > 0:

			if not self.active_timer:
				await self.__event.wait()
				self.__event.clear()
				self.active_timer = True

			try:
				await wait_for(self.__wait_move(), timeout=self.time)
			except TimeoutError:
				await self.own_object.own_object.on_end_timer(self.own_object)

	def flip_the_timer(self):
		"""Меняет положение таймера (активный/деактивный)"""

		self.__event.set()

		if self.active_timer:
			self.time = self.time - (_time() - self.last_flip)
			self.active_timer = False

		return self.time

	def stop_the_timer(self):
		"""Stop the timer"""

		self.time = 0  # timer loop has condition self.time > 0. I'm killing timer loop by changing the condition
		self.flip_the_timer()  # back to loop start and kill timer loop
		self.flip_the_timer()  # if timer in activity position
