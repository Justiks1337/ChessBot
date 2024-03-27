import sqlite3
import aiosqlite
from asyncio import get_event_loop
from config.ConfigValues import ConfigValues
from database_tools.backup_tools import backup
from database_tools.database_log.log import log
import os


class Connection:
	"""Class connection - центр управления базой данных"""

	def __init__(self):
		loop = get_event_loop()
		self.connection: aiosqlite.Connection
		self.__transactions: int = 0
		loop.run_until_complete(self.__on_connect())
		log.info(f'successful connect to {ConfigValues.db_name}')

	async def __on_connect(self):
		self.connection = await aiosqlite.connect(str(os.path.join(os.path.dirname(__file__), ConfigValues.db_name)))
		await self.request(
			"""CREATE TABLE IF NOT EXISTS "users" (
			"user_id"	INTEGER NOT NULL UNIQUE,
			"games"	INTEGER,
			"points"	INTEGER,
			"nickname"	TEXT,
			"username"	TEXT,
			"session_id"	TEXT,
			"ip_address"	TEXT,
			PRIMARY KEY("user_id")
		)""")

		await self.request("""CREATE TABLE IF NOT EXISTS "games" (
			"first_player"	INTEGER NOT NULL,
			"second_player"	INTEGER NOT NULL,
			"winner" INTEGER NOT NULL,
			FOREIGN KEY("second_player") REFERENCES "users"("user_id"),
			FOREIGN KEY("winner") REFERENCES "users"("user_id"),
			FOREIGN KEY("first_player") REFERENCES "users"("user_id")
		)""")

		await self.request("""CREATE TABLE IF NOT EXISTS "blacklist" (
			"user_id"	INTEGER NOT NULL,
			"username"	TEXT NOT NULL,
			FOREIGN KEY("user_id") REFERENCES "users"("user_id")
		)""")

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

		log.debug(
			f'request to {ConfigValues.db_name}. sql_request: {sql_request}, values: {values}, transaction: {self.__transactions}')

		return statement


connect: Connection = Connection()
