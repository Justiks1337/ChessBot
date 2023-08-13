from channels.generic.websocket import AsyncJsonWebsocketConsumer

from core import get
from Game import games


class UserWebsocket(AsyncJsonWebsocketConsumer):
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

    async def update_board(self, event):
        session_id = self.scope["session"]["session_id"]

        user = get(games, 'players', session_id=session_id)
        user.move()

    async def end_timer(self, event):
        await self.send_json({"event": "end_timer", "loser": event['loser']})

    async def mate(self, event):
        await self.send_json({"event": "mate", "winner": event['winner']})

    async def stalemate(self, event):
        await self.send_json({"event": "stalemate"})

    async def draw(self, event):
        await self.send_json({"event": "draw"})

    async def draw_offer(self, event):
        await self.send_json({"event": "draw_offer", "receiver": event['receiver']})
