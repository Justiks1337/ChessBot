from typing import Optional
from time import time as _time
import asyncio

from config.ConfigValues import ConfigValues


class Timer:
	"""class Timer"""

	def __init__(
			self,
			own_object,
			time: int = ConfigValues.game_time,
	):
		self.__event = asyncio.Event()

		self.last_flip = None
		self.own_object = own_object
		self._time = time

	@property
	def time(self):
		return round(self._time)

	async def __wait_move(self):
		"""wait move"""

		self.last_flip = _time()

		waiter_task = asyncio.get_running_loop().create_task(self.__event.wait())
		await waiter_task

		self.__event.clear()

	async def start_timer(self):
		"""Start the timer"""

		loop = asyncio.get_running_loop()

		try:
			await Timer.wait_for(self.__wait_move(), timeout=self._time, loop=loop)
		except asyncio.TimeoutError:

			loop.create_task(self.own_object.own_object.on_end_timer(self.own_object))
			return

	def update_timer(self):

		if not self.last_flip:
			self.last_flip = _time()

		self._time = self._time - (_time() - self.last_flip)
		self.last_flip = _time()

	def flip_the_timer(self):
		"""Меняет положение таймера (активный/деактивный)"""

		self.__event.set()

		self.update_timer()

		return self._time

	@staticmethod
	async def wait_for(task, timeout=0, loop: Optional[asyncio.AbstractEventLoop] = None):

		task = loop.create_task(task)

		await asyncio.sleep(timeout)

		if not task.done():
			raise asyncio.TimeoutError()
