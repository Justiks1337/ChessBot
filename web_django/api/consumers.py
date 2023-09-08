from asyncio import create_task

from channels.generic.websocket import AsyncJsonWebsocketConsumer

from web_django.django_log.log import log
from config.ConfigValues import ConfigValues
from Game import Game


class BotConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):

        for header in self.scope["headers"]:
            if header[0] == b'authorization' and header[1].decode('utf-8') == ConfigValues.server_authkey:
                await self.accept()
                return

        await self.close()

    async def disconnect(self, code):
        for i in range(5):
            log.critical("БОТ ОТКЛЮЧИЛСЯ ОТ ВЕБСОКЕТА! ПРОВЕРЬТЕ СОЕДИНЕНИЕ БОТА!")

    async def receive_json(self, content, **kwargs):
        if content["event"] == "start_game":
            await self.start_game(content)

    async def start_game(self, event):

        game = Game((event["first_user_id"], event["second_user_id"]))

        await self.send_json({
            "event": "start_game",
            "players": [event["first_user_id"], event["second_user_id"]],
            "uuid": game.tag})

        task = create_task(game.start_timers_game())

        await task
