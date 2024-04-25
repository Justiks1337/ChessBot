import os
from typing import Optional
import glob

from chessboards.chess_core.Timer import Timer
from chessboards.models import UserModel


class User:
	"""User class"""

	def __init__(self, user_id: int, color: bool, own_object):
		self.user_id = int(user_id)
		self.color: bool = color
		self.timer: Timer = Timer(self)
		self.color_text = (lambda x: "бел" if x else "чёрн")(self.color)
		self.draw_offer = False
		self.own_object = own_object
		self.avatar_path = None
		self.model_user = None

		self.games: Optional[int] = None
		self.points: Optional[int] = None
		self.nickname: Optional[str] = None
		self.username: Optional[str] = None
		self.session_id: Optional[str] = None
		self.avatar_path: Optional[str] = None

		self.own_object.players.append(self)

	async def fill_attributes(self):
		"""fill attributes from database"""

		self.model_user = await UserModel.objects.aget(user_id=self.user_id)

		self.games = self.model_user.games
		self.points = self.model_user.points
		self.nickname = self.model_user.nickname
		self.username = self.model_user.username

		file_name = glob.glob(f"{os.getenv('PATH_TO_AVATARS')}{self.user_id}.*")

		if len(file_name):
			self.avatar_path = file_name[0][file_name[0].index('avatars/'):]
			return

		self.avatar_path = "avatars/unknown_user.png"

	async def move(self, start_cell: str, end_cell: str):
		"""move in board and flip timer"""

		await self.timer.flip_the_timer()
		await self.own_object.move("".join([start_cell, end_cell]))

	async def draw(self):
		self.draw_offer = True
		await self.own_object.on_draw_offer()

	async def give_up(self):
		await self.own_object.on_give_up(self.user_id)

	async def start_timer(self):
		"""timer starter"""

		await self.timer.start_timer()

	async def remove_games(self):
		"""remove games count after end game"""
		self.model_user.games -= 1
		await self.model_user.asave()

	async def give_points(self):
		"""add points count after end game"""

		self.model_user.games += 1
		await self.model_user.asave()
