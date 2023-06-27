from config.ConfigValues import ConfigValues
from aiohttp import ClientSession
from os import system
from datetime import datetime
from time import time
from database_tools.database_log.log import log
from os import path


def __dump() -> str:
	"""Делает бекап базы данных sqlite
	:return dump filename
							"""
	start_time = time()

	backup_file_name = "mydatabase_backup_" + datetime.now().strftime("%Y%m%d%H%M%S") + '.sql'

	system(
		f'sqlite3 {path.join(path.dirname(__file__), ConfigValues.db_name)} .dump > {path.join(path.dirname(__file__), backup_file_name)}')

	log.info(f'Database dump was completed in {time() - start_time} seconds')

	return backup_file_name


async def backup():
	"""backup to Yadisk"""

	backup_name = __dump()

	async with ClientSession() as session:
		async with session.get(
			f"https://cloud-api.yandex.net/v1/disk/resources/upload?path={backup_name}&overwrite=true",
			headers={
				"Content-Type": "application/json",
				"Accept": "application/json",
				"Authorization": f'{ConfigValues.yadisk_jwt}'}
		) as response:
			async with session.put((await response.json())['href'], data=open(backup_name, "rb")) as resp:

				log.info(f'The database backup has been completed. Database dump is named as {backup_name}')

				return await resp.json(content_type=None)
