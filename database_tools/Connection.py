import sqlite3
import aiosqlite
from asyncio import new_event_loop
from config.ConfigValues import ConfigValues
from backup_tools import backup
from database_log.log import log


class Connection:
	"""Class connection - центр управления базой данных"""

	def __init__(self):
		self.connection: aiosqlite.Connection = new_event_loop().run_until_complete(aiosqlite.connect(ConfigValues.db_name))
		self.__transactions: int = 0

		log.info(f'successful connect to {ConfigValues.db_name}')

	async def __on_request(self, sql_request: str):
		"""Coro handler on_request(sql_request: str)
			Works after request to database
		"""

		if "select" in sql_request.lower():
			return

		self.__transactions += 1
		if self.__transactions == ConfigValues.transactions_to_backup:
			self.__transactions = 0
			await backup()

	async def request(self, sql_request: str, values=()) -> sqlite3.Cursor:
		"""coro request(sql_request, values)

			:arg sql_request - Your sql request
			:arg values - Value for substitution

			:return sqlite3.Cursor

			Ex:
				values = await (await request("SELECT user_id FROM users WHERE balance = ?"), (100, )).fetchall()
		"""

		cursor = await self.connection.cursor()
		statement = await cursor.execute(sql_request, values)

		await self.connection.commit()
		await self.__on_request(sql_request)

		log.debug(f'request to {ConfigValues.db_name}. sql_request: {sql_request}, values: {values}')

		return statement


connect: Connection = Connection()
