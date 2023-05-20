from Game import Game


class Queue:
	"""Класс - очередь (единственный экземпляр создаётся в main.py"""

	def __init__(self):
		self.users = []

	def add_new_user(self, user_id: int):
		"""Добавляет нового игрока в очередь"""

		self.users.append(user_id)

	def start_game(self):
		"""Начало игры"""

		Game((self.users[0], self.users[1]))
		self.users.clear()

	def on_new_user(self):
		"""Хандлер срабатывающий при попадании нового пользователя в очередь"""

		if len(self.users) == 2:
			self.start_game()

	def leave_from_queue(self, user_id: int):
		"""Удаляет участника из очереди"""

		self.users.remove(user_id)
