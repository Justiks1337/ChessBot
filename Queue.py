from asyncio import create_task
from queue import Queue as PyQueue

from aiohttp import ClientSession

from config.ConfigValues import ConfigValues
from database_tools.Connection import connect
from OrderedSet import OrderedSet
from Bot import Bot


class Queue(PyQueue):
	"""Класс - очередь (единственный экземпляр создаётся в main.py"""

	# rewriting implementation
	def _init(self, maxsize):
		self.queue: OrderedSet = OrderedSet()

	def _put(self, item):
		self.queue.add(item)

	def _get(self):
		return self.queue.pop()

	async def add_new_user(self, bot: Bot, user_id: int):
		"""Добавляет нового игрока в очередь"""

		try:
			await self.checks(user_id)
		except AssertionError as error:
			await bot.send_message(user_id, error.args[0])
			return

		try:
			self.put(user_id)
		except KeyError:
			await bot.send_message(user_id, ConfigValues.if_in_queue)
			return

		await create_task(bot.send_message(user_id, ConfigValues.on_queue_join_message))
		await create_task(self.on_new_user(bot))

	async def start_game(self, bot: Bot):
		"""Начало игры"""

		users = [self.get(), self.get()]

		await bot.websocket_connection.send({
			"event": "start_game",
			"first_user_id": users[0],
			"second_user_id": users[1]})

	async def on_new_user(self, bot: Bot):
		"""Хандлер срабатывающий при попадании нового пользователя в очередь"""

		if self.full():
			await create_task(self.start_game(bot))

	async def checks(self, user_id):
		await Queue.check_games_amount(user_id)
		await Queue.check_in_game(user_id)

	@staticmethod
	async def check_games_amount(user_id):

		games = await (await connect.request("SELECT games FROM users WHERE user_id = ?", (user_id, ))).fetchone()

		assert games[0], ConfigValues.if_games_not_enough

	@staticmethod
	async def check_in_game(user_id):
		async with ClientSession() as session:
			async with session.post(
					f"http://{ConfigValues.server_ip}:{ConfigValues.server_port}/api/v1/check_in_game",
					params={"user_id": user_id},
					headers={
						"content-type": "application/json",
						"Authorization": ConfigValues.server_authkey}) as response:

				json = await response.json()

				assert not json['in_game'], ConfigValues.in_game_error

	def leave_from_queue(self, user_id: int):
		"""Удаляет участника из очереди"""

		del self.queue.map[user_id]


main_queue = Queue(maxsize=2)
