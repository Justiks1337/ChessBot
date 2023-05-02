import uuid
from DatabaseAssistant import request
from asyncio import sleep, get_event_loop
from Timer import Timer


class User:
	def __init__(self, telegram_id: int, color: bool):
		self.telegram_id: int = telegram_id
		self.color: bool = color
		self.custom_page: str = self.generate_unique_key()
		self.timer: Timer = Timer()

	@staticmethod
	def generate_unique_key() -> str:
		""":return уникальный ключ"""
		return str(uuid.uuid4())

	async def database_fill(self):
		await request("UPDATE users SET games = games - 1 WHERE user_id = ?", (self.telegram_id, ))
