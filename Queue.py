from asyncio import create_task

from aiohttp import ClientSession
from aiogram import Bot

from config.ConfigValues import ConfigValues
from database_tools.Connection import connect


class Queue:
	"""Класс - очередь (единственный экземпляр создаётся в main.py"""

	def __init__(self):
		self.users = []

	async def add_new_user(self, bot: Bot, user_id: int):
		"""Добавляет нового игрока в очередь"""

		try:
			await self.checks(user_id)
		except AssertionError as error:
			await bot.send_message(user_id, error.args[0])
			return

		self.users.append(user_id)
		await create_task(bot.send_message(user_id, ConfigValues.on_queue_join_message))
		await create_task(self.on_new_user(bot))

	@staticmethod
	async def start_game(bot: Bot, users: list):
		"""Начало игры"""
		async with ClientSession() as session:
			async with session.post(
					f"http://{ConfigValues.server_ip}:{ConfigValues.server_port}/api/v1/start_game",
					params={
						"first_user_id": users[0],
						"second_user_id": users[1]},
					headers={
						"content-type": "application/json",
						"Authorization": ConfigValues.server_authkey}) as response:

				json = await response.json()

				url = f'http://{ConfigValues.server_ip}:{ConfigValues.server_port}/playgrounds/games/{json["uuid"]}'

				for user_id in users:
					await bot.send_message(user_id, ConfigValues.on_find_enemy.replace('{url}', url))

	async def on_new_user(self, bot: Bot):
		"""Хандлер срабатывающий при попадании нового пользователя в очередь"""

		if len(self.users) == 2:
			await create_task(self.start_game(bot, self.users))
			self.users.clear()

	async def checks(self, user_id):
		self.check_in_queue(user_id)
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

	def check_in_queue(self, user_id):
		assert user_id not in self.users, ConfigValues.if_in_queue

	def leave_from_queue(self, user_id: int):
		"""Удаляет участника из очереди"""

		self.users.remove(user_id)


main_queue = Queue()
