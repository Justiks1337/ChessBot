from asyncio import sleep, get_event_loop
from datetime import timedelta


class Timer:
	def __init__(self):
		self.timer = get_event_loop().run_until_complete(self.start_timer())

	async def start_timer(self):
		self.timer = 900
		while bool(self.timer):
			self.timer = self.timer - 1
			await sleep(1)

	def to_time(self):
		return timedelta(seconds=self.timer)


