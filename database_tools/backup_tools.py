from config import db_name, yadisk_jwt
from aiohttp import ClientSession
from os import system
from datetime import datetime
from asyncio import run


async def __dump() -> str:
	backup_file_name = "mydatabase_backup_" + datetime.now().strftime("%Y%m%d%H%M%S") + '.sql'

	system(f'sqlite3 {db_name} .dump > {backup_file_name}')

	return backup_file_name


async def backup():
	backup_name = await __dump()

	async with ClientSession() as session:
		async with session.get(
			f"https://cloud-api.yandex.net/v1/disk/resources/upload?path={backup_name}&overwrite=true",
			headers={
				"Content-Type": "application/json",
				"Accept": "application/json",
				"Authorization": f'{yadisk_jwt}'}
		) as response:
			async with session.put((await response.json())['href'], data=open(backup_name, "rb")) as resp:
				return await resp.json(content_type=None)
