from configparser import ConfigParser as _ConfigParser
import os


class ConfigValues:
	"""Get values from config"""

	__config_file = _ConfigParser()
	__config_file.read(os.path.join(os.path.dirname(__file__), 'config.ini'))

	# database section
	db_name = __config_file.get('database', 'db_name')
	transactions_to_backup = __config_file.get('database', 'transactions_to_backup')

	# Yadisk section
	yadisk_jwt = __config_file.get('Yadisk', 'yadisk_jwt')

	# Telegram section
	telegram_token = __config_file.get('Telegram', 'telegram_token')

	# Messages
