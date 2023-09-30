import asyncio
from uuid import uuid4
from time import time
from typing import Optional

import chess
from channels.consumer import get_channel_layer

from User import User
from config.ConfigValues import ConfigValues
from database_tools.Connection import connect


class Game:
	"""Класс отвечающий за игру"""

	def __init__(self, users_ids: tuple):
		self.board: chess.Board = chess.Board()
		self.players: list = []
		self.player_1: User = User(users_ids[0], True, self)
		self.player_2: User = User(users_ids[1], False, self)
		self._started_at = time()
		self.tag = str(uuid4())

		games.append(self)

	@property
	def started_at(self):
		return round(self._started_at)

	async def move(self, text_move):
		""":raise BaseError если на доске ситуация приводящая к концу игры либо противоречащая её продолжению"""

		turn_player = self.get_turn_player()

		try:

			self.board.push_san(text_move)
		except chess.IllegalMoveError as error:
			if "missing promotion piece type" in error.args[0]:
				self.board.push_san(f"{text_move}q")
			else:
				raise chess.IllegalMoveError()

		asyncio.get_running_loop().create_task(self.get_turn_player().start_timer(), name=self.tag)

		turn_player.timer.flip_the_timer()

		await channel_layer.group_send(
			self.tag,
			{
				"type": "update_board",
				"board": self.board.board_fen(),
				"first_user_time": 	self.player_1.timer.time,
				"second_user_time": self.player_2.timer.time
			}
		)

		await self.move_checks()

		return self.board.board_fen()

	async def checkmate(self):
		""":raise MateError если есть на доске мат"""

		if self.board.is_checkmate():
			winner = self.get_winner()
			await self.on_end_game(ConfigValues.on_mate_message.replace('{color}', winner.color_text))
			await self.on_win(winner)

	async def check_stalemate(self):
		""":raise DrawError если на доске пат"""

		if self.board.is_stalemate():
			await self.on_end_game(ConfigValues.on_stalemate_message)

	async def on_check(self):
		if self.board.is_check():
			await channel_layer.group_send(
				self.tag,
				{
					'type': 'on_check',
					'recipient': self.get_turn_player().user_id
				}
			)

	async def move_checks(self):
		await self.checkmate()
		await self.check_stalemate()
		await self.on_check()

	def get_winner(self) -> User:
		""":return User - object"""

		return self.player_1 if not self.board.turn else self.player_2

	def get_turn_player(self):
		""":return User object"""

		return self.player_1 if self.player_1.color is self.board.turn else self.player_2

	async def start_timers_game(self):
		"""actions before start game"""

		for player in self.players:
			asyncio.get_running_loop().create_task(player.fill_attributes())

		await asyncio.sleep(ConfigValues.prepare_time)

		asyncio.get_running_loop().create_task(self.get_turn_player().start_timer(), name=self.tag)

	async def on_end_game(self, message):
		"""Коро хендлер срабатывающий после окончания игры"""

		self.delete_timers()

		await channel_layer.group_send(
			self.tag,
			{
				'type': "end_game_event",
				'message': message
			})

		await self.player_1.remove_games()
		await self.player_2.remove_games()

		games.remove(self)

	def delete_timers(self):
		for task in asyncio.all_tasks(asyncio.get_running_loop()):
			if task.get_name() == self.tag:
					task.cancel()

	async def on_win(self, winner: User):
		await winner.give_points()
		await self.add_to_game_registry(winner)

	async def on_draw(self):
		await self.add_to_game_registry(None)

	async def add_to_game_registry(self, winner: Optional[User]):

		await connect.request("INSERT INTO games VALUES (?, ?, ?)", (
			self.player_1.user_id,
			self.player_2.user_id,
			winner.user_id))

	async def on_draw_offer(self):
		for player in self.players:
			if not player.draw_offer:

				await channel_layer.group_send(
					self.tag,
					{
						'type': "draw_offer_event",
						'recipient': player.user_id
					}
				)
				return

		await self.on_end_game(ConfigValues.on_draw_message)

	async def on_give_up(self, user_id: int):
		for player in self.players:
			if player.user_id != user_id:
				await self.on_win(player)
			else:
				await self.on_end_game(ConfigValues.on_resign.replace('{color}', player.color_text))

	async def on_end_timer(self, loser: User):

		# noinspection PyTypeChecker
		await self.on_win((lambda player: self.player_1 if player == self.player_2 else self.player_2)(loser))

		await self.on_end_game(ConfigValues.on_end_time.replace('{color}', loser.color_text))


channel_layer = get_channel_layer("default")
games = []
