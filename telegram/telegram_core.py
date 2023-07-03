from database_tools.Connection import connect
from config.ConfigValues import ConfigValues


def in_blacklist(func):
	"""Check user in blacklist"""

	async def wrapped(*args, **kwargs):
		if (await (
				await connect.request("SELECT user_id FROM blacklist WHERE username = ?", (args[1].from_user.username, ))
		).fetchone()):
			return await args[0].send_message(args[1].chat.id, ConfigValues.on_blacklsit_message)

		return await func(*args, **kwargs)

	return wrapped
