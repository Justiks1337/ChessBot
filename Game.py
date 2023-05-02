from User import User



class Game:
	def __init__(self, users_ids: tuple):
		self.pole = None
		self.player_1: User = User(users_ids[0], True)
		self.player_2: User = User(users_ids[1], False)

