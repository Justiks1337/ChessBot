from typing import Optional
import glob

from chess_core.UserId import UserId
from config.ConfigValues import ConfigValues
from database_tools.Connection import connect
from chess_core.Timer import Timer


class User:
	"""User class"""

	def __init__(self, user_id: int, color: bool, own_object):
		self._user_id: UserId = UserId(user_id)
		self.color: bool = color
		self.timer: Timer = Timer(self)
		self.color_text = (lambda x: "бел" if x else "чёрн")(self.color)
		self.draw_offer = False
		self.own_object = own_object

		# attributes from database
		self.games: Optional[int] = None
		self.points: Optional[int] = None
		self.nickname: Optional[str] = None
		self.username: Optional[str] = None
		self.session_id: Optional[str] = None
		self.avatar_path: Optional[str] = None

		self.own_object.players.append(self)

	@property
	def user_id(self):
		return self._user_id.user_id

	async def fill_attributes(self):
		"""fill attributes from database"""

		info = await (await connect.request(
			"SELECT games, points, nickname, username, session_id FROM users WHERE user_id = ?",
			(self.user_id,)
		)).fetchone()

		self.games = info[0]
		self.points = info[1]
		self.nickname = info[2]
		self.username = info[3]
		self.session_id = info[4]

		file_name = glob.glob(f"{ConfigValues.path_to_avatars}{self.user_id}.*")

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

		await connect.request("UPDATE users SET games = games - 1 WHERE user_id = ?", (self.user_id, ))

	async def give_points(self):
		"""add points count after end game"""

		await connect.request("UPDATE users SET points = points + 1 WHERE user_id = ?", (self.user_id, ))
