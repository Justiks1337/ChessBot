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
	authorization_instructions = __config_file.get('Messages', 'authorization_instructions')
	game_instructions = __config_file.get('Messages', 'game_instructions')
	on_queue_join_message = __config_file.get('Messages', 'on_queue_join_message')
	on_queue_leave_message = __config_file.get('Messages', 'on_queue_leave_message')
	profile_message = __config_file.get('Messages', 'profile_message')
	dashboard_title = __config_file.get('Messages', 'dashboard_title')
	dashboard_object = __config_file.get('Messages', 'dashboard_object')
	dashboard_on_range_error = __config_file.get('Messages', 'dashboard_on_range_error')
	authorization_message = __config_file.get('Messages', 'authorization_message')
	illegal_move_error = __config_file.get('Messages', 'illegal_move_error')
	on_mate_message = __config_file.get('Messages', 'on_mate_message')
	on_draw_message = __config_file.get('Messages', 'on_draw_message')
	on_end_time = __config_file.get('Messages', 'on_end_time')

	# Game

	game_time = __config_file.get('Game', 'game_time')
