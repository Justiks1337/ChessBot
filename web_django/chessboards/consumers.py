from channels.generic.websocket import AsyncJsonWebsocketConsumer
from asgiref.sync import sync_to_async
from chess import IllegalMoveError
from autobahn.exception import Disconnected

from chess_core.core import get
from config.ConfigValues import ConfigValues
from chess_core.Game import games
from web_django.django_log.log import log


class UserWebsocket(AsyncJsonWebsocketConsumer):

    async def connect(self):

        self.board_tag = self.scope['url_route']['kwargs']['tag']
        self.sessionid = await self.get_sessionid()
        self.user = await get(games, 'players', session_id=self.sessionid)

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

        await self.close()

    async def receive_json(self, content, **kwargs):

        # switch case construction does not exit in python 3.9 so:

        if content["type"] == "draw_offer":
            await self.draw_offer()
        elif content["type"] == "give_up":
            await self.give_up()
        elif content["type"] == "move":
            await self.move(content["start_cell"], content["end_cell"])
        elif content["type"] == "get_legal_moves":
            await self.get_legal_moves(content["figure_cell"])

    async def send_json(self, content, close=False):
        try:
            await super().send_json(content, close=close)
        except Disconnected:
            log.info("autobahn.exception.Disconnection error. ")

    async def end_game_event(self, event):
        await self.send_json({"event": 'end_game', "message": event['message']})
        await self.disconnect(200)

    async def draw_offer_event(self, event):
        await self.send_json({"event": "draw_offer", "recipient": event['recipient']})

    async def on_check(self, event):
        await self.send_json({"event": "on_check", "recipient": event['recipient']})

    async def update_board(self, event):
        await self.send_json({
            "event": "update_board",
            "board": event["board"],
            "first_user_time": round(event["first_user_time"]),
            "second_user_time": round(event["second_user_time"])})

    async def illegal_move_error(self, message):
        await self.send_json({"event": "illegal_move_error", "message": message})

    async def error(self, message):
        await self.send_json({"event": "error", "message": message})

    async def move(self, start_cell: str, end_cell: str):

        if not self.user:
            return

        if self.user.own_object.board.turn is not self.user.color:
            await self.error(ConfigValues.on_illegal_action_error)
            return

        try:
            await self.user.move(start_cell, end_cell)
        except IllegalMoveError:
            await self.illegal_move_error(ConfigValues.illegal_move_error)

    async def get_legal_moves(self, figure_cell: str):

        if not self.user:
            return

        cells = self.user.own_object.get_legal_moves(figure_cell)

        await self.send_json({"event": "legal_moves", "cells": cells})

    async def draw_offer(self):

        if not self.user:
            return

        await self.user.draw()

    async def give_up(self):

        if not self.user:
            return

        await self.user.give_up()

    @sync_to_async()
    def get_sessionid(self):
        headers = self.scope["headers"]

        for header in headers:
            if header[0] == b'cookie':
                sessionid = header[1].decode("utf-8")
                return sessionid.replace('sessionid=', '')
