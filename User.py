from typing import Optional
from os.path import exists

from database_tools.Connection import connect
from Timer import Timer


class User:
	"""User class"""

	def __init__(self, user_id: int, color: bool, own_object):
		self.user_id: int = user_id
		self.color: bool = color
		self.timer: Timer = Timer(self, color)
		self.color_text = lambda x: "бел" if x else "чёрн"
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

		if exists(f"web_django/static/avatars/{self.user_id}.png"):
			self.avatar_path = f"avatars/{self.user_id}.png"
			return

		self.avatar_path = "avatars/unknown_user.png"

	async def move(self, start_cell: str, end_cell: str):
		"""move in board and flip timer"""

		await self.own_object.move("".join([start_cell, end_cell]))

	async def draw(self):
		self.draw_offer = True
		await self.own_object.on_draw_offer()

	async def give_up(self):
		await self.own_object.on_give_up(self.user_id)

	def timer_continue(self):
		"""return timer to activity"""

		self.timer.flip_the_timer()

	def stop_timer(self):
		"""kill timer (fatal stop)"""

		self.timer.stop_the_timer()

	async def start_timer(self):
		"""timer starter"""

		await self.timer.start_timer()

	async def remove_games(self):
		"""remove games count after end game"""

		await connect.request("UPDATE users SET games = games - 1 WHERE user_id = ?", (self.user_id, ))

	async def give_points(self):
		"""add points count after end game"""

		await connect.request("UPDATE users SET points = points + 1 WHERE user_id = ?", (self.user_id, ))
