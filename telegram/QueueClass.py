from asyncio import create_task
from queue import Queue as PyQueue

from aiohttp import ClientSession

from config.ConfigValues import ConfigValues
from decorators import send_message
from telegram.database import Connection


class Queue(PyQueue):
	"""Класс - очередь (единственный экземпляр создаётся в __init__.py"""

	# rewriting implementation
	def __init__(self, maxsize):
		super().__init__(maxsize)
		self.queue: set = set()

	def _put(self, item):
		self.queue.add(item)

	def _get(self):
		return self.queue.pop()

	async def add_new_user(self, user_id: int):
		"""Добавляет нового игрока в очередь"""

		try:
			await self.checks(user_id)
		except AssertionError as error:
			await send_message(user_id, error.args[0])
			return

		self.put(user_id)

		send_task = create_task(send_message(user_id, ConfigValues.on_queue_join_message))
		new_user_task = create_task(self.on_new_user())

		await new_user_task
		await send_task

	def leave_from_queue(self, user_id: int):
		"""Удаляет участника из очереди"""

		self.queue.remove(user_id)

	async def on_new_user(self):
		"""Хандлер срабатывающий при попадании нового пользователя в очередь"""
		if self.full():
			await self.start_game()

	async def start_game(self):
		"""Начало игры """

		users = [self.get(), self.get()]

		async with ClientSession() as session:
			async with session.post(
					f"{ConfigValues.server_http_protocol}://{ConfigValues.server_ip}/api/v1/start_game",
					headers={
						"content-type": "application/json",
						"Authorization": ConfigValues.server_authkey},
					json={"players": [users[0], users[1]]}) as response:

				json = await response.json()

				url = f"{ConfigValues.proxy_http_protocol}://{ConfigValues.proxy_ip}\
{ConfigValues.url_to_playground.replace('{rout}', json['uuid'])}"

				for user_id in users:
					await send_message(user_id, ConfigValues.on_find_enemy.replace('{url}', url))

	async def checks(self, user_id):
		return self.check_in_queue(user_id)
		await Queue.check_games_amount_deprecated(user_id)
		await Queue.check_in_game(user_id)

	def check_in_queue(self, user_id):
		return user_id not in self.queue, ConfigValues.if_in_queue

	@staticmethod
	async def check_games_amount_deprecated(user_id):

		games = await Connection().connection.fetchrow("SELECT games FROM users WHERE user_id = $1::bigint", user_id, )

		assert games[0], ConfigValues.if_games_not_enough

	@staticmethod
	async def check_in_game(user_id):
		async with ClientSession() as session:
			async with session.post(
					f"{ConfigValues.server_http_protocol}://{ConfigValues.server_ip}/api/v1/check_in_game",
					params={"user_id": user_id},
					headers={
						"content-type": "application/json",
						"Authorization": ConfigValues.server_authkey}) as response:

				json = await response.json()
				assert not json['in_game'], ConfigValues.in_game_error


main_queue = Queue(2)
