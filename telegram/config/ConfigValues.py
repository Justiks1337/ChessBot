from configparser import ConfigParser as _ConfigParser
import os


class ConfigValues:
	"""Get values from config"""

	__config_file = _ConfigParser()
	__config_file.read(os.path.join(os.path.dirname(__file__), 'config.ini'), encoding='utf-8-sig')

	# database section
	database_user = __config_file.get('database', 'database_user')
	database_password = __config_file.get('database', 'database_password')
	database_name = __config_file.get('database', 'database_name')
	database_host = __config_file.get('database', 'database_host')
	database_port = int(__config_file.get('database', 'database_port'))

	# Telegram section
	telegram_token = __config_file.get('Telegram', 'telegram_token')
	admin_ids: list = __config_file.get('Telegram', 'admin_ids').split(', ')
	recharge_time = int(__config_file.get('Telegram', 'recharge_time'))
	authorization_tokens_live_time = int(__config_file.get('Telegram', 'authorization_tokens_live_time'))

	# Messages
	authorization_instructions = __config_file.get('Messages', 'authorization_instructions').replace('\\n', '\n')
	game_instructions = __config_file.get('Messages', 'game_instructions').replace('\\n', '\n')
	manual = __config_file.get('Messages', 'manual').replace('\\n', '\n')
	on_queue_join_message = __config_file.get('Messages', 'on_queue_join_message').replace('\\n', '\n')
	on_queue_leave_message = __config_file.get('Messages', 'on_queue_leave_message').replace('\\n', '\n')
	only_in_dm_message = __config_file.get('Messages', 'only_in_dm_message').replace('\\n', '\n')
	if_in_queue = __config_file.get('Messages', 'if_in_queue').replace('\\n', '\n')
	if_not_in_queue = __config_file.get('Messages', 'if_not_in_queue').replace('\\n', '\n')
	if_games_not_enough = __config_file.get('Messages', 'if_games_not_enough').replace('\\n', '\n')
	in_game_error = __config_file.get('Messages', 'in_game_error').replace('\\n', '\n')
	profile_message = __config_file.get('Messages', 'profile_message').replace('\\n', '\n')
	dashboard_title = __config_file.get('Messages', 'dashboard_title').replace('\\n', '\n')
	dashboard_object = __config_file.get('Messages', 'dashboard_object').replace('\\n', '\n')
	dashboard_on_range_error = __config_file.get('Messages', 'dashboard_on_range_error').replace('\\n', '\n')
	illegal_move_error = __config_file.get('Messages', 'illegal_move_error').replace('\\n', '\n')
	on_mate_message = __config_file.get('Messages', 'on_mate_message').replace('\\n', '\n')
	on_stalemate_message = __config_file.get('Messages', 'on_stalemate_message').replace('\\n', '\n')
	on_draw_message = __config_file.get('Messages', 'on_draw_message').replace('\\n', '\n')
	on_end_time = __config_file.get('Messages', 'on_end_time').replace('\\n', '\n')
	on_someone_move = __config_file.get('Messages', 'on_someone_move').replace('\\n', '\n')
	on_resign = __config_file.get('Messages', 'on_resign').replace('\\n', '\n')
	authorization_message = __config_file.get('Messages', 'authorization_message').replace('\\n', '\n')
	success_authorization_message = __config_file.get('Messages', 'success_authorization_message').replace('\\n', '\n')
	on_authorization_error = __config_file.get('Messages', 'on_authorization_error').replace('\\n', '\n')
	on_delete_authorization_code = __config_file.get('Messages', 'on_delete_authorization_code').replace('\\n', '\n')
	on_unsuccessful_authorization_message = __config_file.get('Messages', 'on_unsuccessful_authorization_message').replace('\\n', '\n')
	unauthorized_message = __config_file.get('Messages', 'unauthorized_message').replace('\\n', '\n')
	on_blacklist_message = __config_file.get('Messages', 'on_blacklist_message').replace('\\n', '\n')
	on_is_not_admin = __config_file.get('Messages', 'on_is_not_admin').replace('\\n', '\n')
	successful_add_to_blacklist = __config_file.get('Messages', 'successful_add_to_blacklist').replace('\\n', '\n')
	successful_remove_from_blacklist = __config_file.get('Messages', 'successful_remove_from_blacklist').replace('\\n', '\n')
	on_invalid_args = __config_file.get('Messages', 'on_invalid_args').replace('\\n', '\n')
	on_find_enemy = __config_file.get('Messages', 'on_find_enemy').replace('\\n', '\n')
	in_recharge = __config_file.get('Messages', 'in_recharge').replace('\\n', '\n')
	on_illegal_action_error = __config_file.get('Messages', 'on_illegal_action_error').replace('\\n', '\n')

	# Game

	prepare_time = int(__config_file.get('Game', 'prepare_time'))
	game_time = int(__config_file.get('Game', 'game_time'))

	# Web

	path_to_avatars = __config_file.get('Web', 'path_to_avatars')
	url_to_playground = __config_file.get('Web', 'url_to_playground').replace('\\n', '\n')
	bot_websocket = __config_file.get('Web', 'bot_websocket').replace('\\n', '\n')
	server_ip = __config_file.get('Web', 'server_ip').replace('\\n', '\n')
	proxy_ip = __config_file.get('Web', 'proxy_ip').replace('\\n', '\n')
	server_port = int(__config_file.get('Web', 'server_port'))
	server_http_protocol = __config_file.get('Web', 'server_http_protocol')
	proxy_http_protocol = __config_file.get('Web', 'proxy_http_protocol')
	websocket_protocol = __config_file.get('Web', 'websocket_protocol')
	server_authkey = __config_file.get('Web', 'server_authkey')
