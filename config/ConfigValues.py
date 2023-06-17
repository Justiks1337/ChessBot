from configparser import ConfigParser as _ConfigParser
import os


class ConfigValues:
	"""Get values from config"""

	__config_file = _ConfigParser()
	__config_file.read(os.path.join(os.path.dirname(__file__), 'config.ini'), encoding='utf-8')

	# database section
	db_name = __config_file.get('database', 'db_name')
	transactions_to_backup = __config_file.get('database', 'transactions_to_backup')

	# Yadisk section
	yadisk_jwt = __config_file.get('Yadisk', 'yadisk_jwt')

	# Telegram section
	telegram_token = __config_file.get('Telegram', 'telegram_token')

	# Messages
	authorization_instructions = __config_file.get('Messages', 'authorization_instructions').replace('\n', '\n')
	game_instructions = __config_file.get('Messages', 'game_instructions').replace('\\n', '\n')
	on_queue_join_message = __config_file.get('Messages', 'on_queue_join_message').replace('\\n', '\n')
	on_queue_leave_message = __config_file.get('Messages', 'on_queue_leave_message').replace('\\n', '\n')
	profile_message = __config_file.get('Messages', 'profile_message').replace('\\n', '\n')
	dashboard_title = __config_file.get('Messages', 'dashboard_title').replace('\\n', '\n')
	dashboard_object = __config_file.get('Messages', 'dashboard_object').replace('\\n', '\n')
	dashboard_on_range_error = __config_file.get('Messages', 'dashboard_on_range_error').replace('\\n', '\n')
	authorization_message = __config_file.get('Messages', 'authorization_message').replace('\\n', '\n')
	illegal_move_error = __config_file.get('Messages', 'illegal_move_error').replace('\\n', '\n')
	on_mate_message = __config_file.get('Messages', 'on_mate_message').replace('\\n', '\n')
	on_draw_message = __config_file.get('Messages', 'on_draw_message').replace('\\n', '\n')
	on_end_time = __config_file.get('Messages', 'on_end_time').replace('\\n', '\n')

	# Game

	game_time = __config_file.get('Game', 'game_time')
