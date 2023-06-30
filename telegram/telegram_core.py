from aiogram.bot import Bot


async def download_user_avatar(bot: Bot, user_id: int):
	"""Download user profile photo

	:arg bot - bot object
	:arg user_id - user id
	"""

	user_profile_photo = await bot.get_user_profile_photos(user_id)

	file = await bot.get_file(user_profile_photo.photos[0][0].file_id)
	await bot.download_file(file.file_path, f'{user_id}.png')
