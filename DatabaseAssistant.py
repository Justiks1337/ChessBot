import aiosqlite
import sqlite3
from asyncio import get_event_loop


async def connection() -> aiosqlite.core.Connection:
	"""await connection() - coro
	Безопасный и умный коннект к базе данных """
	return await aiosqlite.connect("database.db")


class Statement:
	def __init__(self, statement: sqlite3.Cursor):
		self.statement: aiosqlite.core.Cursor = statement

	async def fetchone(self):
		""":return первое найденное значение"""
		return await self.statement.fetchone()

	async def fetchmany(self, amount: int):
		""":return несколько найденных значений"""
		return await self.statement.fetchmany(amount)

	async def fetchall(self):
		""":return все найденные значения """
		return await self.statement.fetchall()


async def request(sql_request: str, values=()) -> Statement:
	""":arg sql_request - SQL запрос
	:arg values - Значения замещающие ? в SQL запросе"""

	cursor = await connect.cursor()
	statement = await cursor.execute(sql_request, values)
	await connect.commit()
	return Statement(statement)


main_loop = get_event_loop()
connect: aiosqlite.core.Connection = main_loop.run_until_complete(connection())
