from asyncio import sleep
import json

import websockets
from aiogram import Bot

from config.ConfigValues import ConfigValues


class BotWebsocket:
    def __init__(self, own_object):

        self.own_object: Bot = own_object

        self.websocket_connection = None

    async def connect(self):

        await sleep(3)

        async with websockets.connect(
                f"ws://{ConfigValues.server_ip}:{ConfigValues.server_port}/{ConfigValues.bot_websocket}",
                extra_headers={"Authorization": ConfigValues.server_authkey}
                ) as websocket:

            self.websocket_connection = websocket

            while True:
                try:
                    await self.on_message(json.loads(await websocket.recv()))
                except Exception:
                    await self.connect()

    async def on_message(self, message: dict):
        print(message)
        if message["event"] == "start_game":
            await self.start_game_event(message)

    async def start_game_event(self, message: dict):

        url = f'http://{ConfigValues.server_ip}:{ConfigValues.server_port}/playgrounds/games/{message["uuid"]}'

        for player_id in message["players"]:
            await self.own_object.send_message(player_id, ConfigValues.on_find_enemy.replace('{url}', url))

    async def send(self, message):
        await self.websocket_connection.send(json.dumps(message))
