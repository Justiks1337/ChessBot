from Game import Game
from aiogram import Bot
from config.ConfigValues import ConfigValues
from exceptions.InQueueError import InQueueError


class Queue:
	"""Класс - очередь (единственный экземпляр создаётся в main.py"""

	def __init__(self):
		self.users = []

	async def add_new_user(self, bot: Bot, user_id: int):
		"""Добавляет нового игрока в очередь"""

		if user_id not in self.users:
			self.users.append(user_id)
			await self.on_new_user(bot, user_id)
			await bot.send_message(user_id, ConfigValues.on_queue_join_message)
			return

		await bot.send_message(user_id, ConfigValues.if_in_queue)

	def start_game(self):
		"""Начало игры"""

		Game((self.users[0], self.users[1]))
		self.users.clear()

	async def on_new_user(self, bot: Bot, user_id: int):
		"""Хандлер срабатывающий при попадании нового пользователя в очередь"""

		if len(self.users) == 2:
			self.start_game()

	def leave_from_queue(self, user_id: int):
		"""Удаляет участника из очереди"""

		self.users.remove(user_id)


main_queue = Queue()
