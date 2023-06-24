from config.ConfigValues import ConfigValues
from asyncio import Event, wait_for, TimeoutError
from time import time as _time
from core import on_end_time_error


class Timer:
	"""class Timer"""

	def __init__(
			self,
			time: int = int(ConfigValues.game_time),
			on_end_time_func=on_end_time_error,  # Function should have *args and **kwargs
			*args,
			**kwargs
	):
		self.__function = on_end_time_func
		self.__initialize = False
		self.__function_args = args
		self.__function_kwargs = kwargs
		self.__event = Event()

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
			if self.__initialize:
				await self.__event.wait()
				self.__event.clear()
			else:
				self.__initialize = True

			try:
				await wait_for(self.__wait_move(), timeout=self.time)
			except TimeoutError:
				self.__function(*self.__function_args, **self.__function_kwargs)

	def flip_the_timer(self):
		"""Меняет положение таймера (активный/деактивный)"""

		self.__event.set()

	def stop_the_timer(self):
		"""Stop the timer"""

		self.time = 0  # timer loop has condition self.time > 0. I'm killing timer loop by changing the condition
		self.flip_the_timer()  # back to loop start and kill timer loop
		self.flip_the_timer()  # if timer in activity position
