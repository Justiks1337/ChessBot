import uuid
from database_tools.Connection import connect
from Timer import Timer


class User:
	def __init__(self, telegram_id: int, color: bool):
		self.telegram_id: int = telegram_id
		self.color: bool = color
		self.custom_page: str = self.generate_unique_key()
		self.timer = Timer(self.color)

	@staticmethod
	def generate_unique_key() -> str:
		""":return уникальный ключ"""
		return str(uuid.uuid4())

	async def database_fill(self):
		await connect.request("UPDATE users SET games = games - 1 WHERE user_id = ?", (self.telegram_id, ))

	def get_color(self):
		return "белых" if self.color else "чёрных"
