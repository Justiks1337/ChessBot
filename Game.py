import asyncio
from uuid import uuid4
from time import time

import chess
from channels.consumer import get_channel_layer

from User import User


class Game:
	"""Класс отвечающий за игру"""

	def __init__(self, users_ids: tuple):
		self.board: chess.Board = chess.Board()
		self.player_1: User = User(users_ids[0], True, self)
		self.player_2: User = User(users_ids[1], False, self)
		self.players: list = []
		self.start_time = time()
		self.tag = uuid4()

		games.append(self)

	async def move(self, text_move):
		""":raise BaseError если на доске ситуация приводящая к концу игры либо противоречащая её продолжению"""

		self.board.push_san(text_move)
		await self.checkmate()
		await self.check_stalemate()

		return self.board.board_fen()

	async def checkmate(self):
		""":raise MateError если есть на доске мат"""

		if self.board.is_checkmate():
			await channel_layer.group_send(
				self.tag,
				{
					'type': "mate_event",
					'winner': self.get_winner()
				})

	async def check_stalemate(self):
		""":raise DrawError если на доске пат"""

		if self.board.is_stalemate():
			await channel_layer.group_send(
				self.tag,
				{
					'type': "stalemate_event",
				})

	def get_winner(self) -> User:
		""":return User - object"""

		return self.player_1 if not self.board.turn else self.player_2

	def get_turn_player(self):
		""":return User object"""

		return self.player_1 if self.player_1.color is self.board.turn else self.player_2

	async def start_timers_game(self):
		"""actions before start game"""

		async with asyncio.TaskGroup() as tasks:
			for user in self.players:
				tasks.create_task(user.fill_attributes())
				tasks.create_task(user.start_timer())

	async def on_end_game(self):
		"""Коро хендлер срабатывающий после окончания игры"""

		self.player_1.stop_timer()
		self.player_2.stop_timer()

		await self.player_1.remove_games()
		await self.player_2.remove_games()

		games.remove(self)

	async def on_win(self, winner: User):
		await winner.give_points()

	async def on_draw_offer(self):

		for player in self.players:
			if not player.draw_offer:

				await channel_layer.group_send(
					self.tag,
					{
						'type': "draw_offer_event",
						'receiver': player.session_id
					}
				)

				return

			await self.on_end_game()
			await channel_layer.group_send(
				self.tag,
				{'type': 'draw_event'}
			)

		await self.on_end_game()

	async def on_give_up(self, user_id: int):
		for player in self.players:
			if player.user_id != user_id:
				await self.on_win(player)

		await self.on_end_game()

	async def on_end_timer(self, loser: User):
		await self.on_end_game()

		# noinspection PyTypeChecker
		await self.on_win(lambda player: self.player_1 if loser == self.player_2 else self.player_2)

		await channel_layer.group_send(
			self.tag,
			{
				'type': "end_timer_event",
				'loser': loser.color
			})


channel_layer = get_channel_layer("default")
games = []
