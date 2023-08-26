from channels.generic.websocket import AsyncJsonWebsocketConsumer
from asgiref.sync import sync_to_async

from core import get
from config.ConfigValues import ConfigValues
from Game import games, Game


class UserWebsocket(AsyncJsonWebsocketConsumer):

    legal_action = ()

    async def connect(self):

        self.board_tag = self.scope['url_route']['kwargs']['tag']

        await self.channel_layer.group_add(
            self.board_tag,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.board_tag,
            self.channel_name
        )

    async def receive_json(self, content, **kwargs):
        if not content["type"] in UserWebsocket.legal_action:
            await self.error("event not found/not legal")
            return

        await self.__dict__[content["type"]]()

    async def update_board(self, event):
        session_id = self.scope["session"]["sessionid"]

        user = get(games, 'players', session_id=session_id)
        user.move()

    async def end_timer_event(self, event):
        await self.send_json({"event": "end_timer", "loser": event['loser']})

    async def mate_event(self, event):
        await self.send_json({"event": "mate", "winner": event['winner']})

    async def stalemate_event(self, event):
        await self.send_json({"event": "stalemate"})

    async def draw_event(self, event):
        await self.send_json({"event": "draw"})

    async def draw_offer_event(self, event):
        await self.send_json({"event": "draw_offer", "receiver": event['receiver']})

    async def error(self, message):
        await self.send_json({"event": "error", "message": message})

    async def move(self, start_cell: str, end_cell: str):
        try:

            board: Game = get(games, '', tag=self.board_tag)
            user_object = get(games, 'players', session_id=self.scope["session"]["sessionid"])

            assert user_object
            assert board.board.turn is user_object.color

            fen_board, time = await user_object.move(start_cell, end_cell)

            if not fen_board:
                await self.error(ConfigValues.illegal_move_error)
                return

            await self.channel_layer.group_send(
                self.board_tag,
                {
                    "type": "update_board_event",
                    "board": fen_board,
                    "user_time": time
                }
             )

        except AssertionError:
            await self.error(ConfigValues.on_illegal_action_error)

    async def draw_offer(self):

        try:

            user_object = get(games, 'players', session_id=self.scope["session"]["sessionid"])

            assert user_object

            await user_object.draw()

        except AssertionError:
            await self.error(ConfigValues.on_illegal_action_error)

    async def give_up(self):
        try:

            user_object = get(games, 'players', session_id=self.scope["session"]["sessionid"])

            assert user_object

            await user_object.give_up()

        except AssertionError:
            await self.error(ConfigValues.on_illegal_action_error)
