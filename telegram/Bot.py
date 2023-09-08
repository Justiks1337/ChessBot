from aiogram import Bot as AioBot

from BotWebsocket import BotWebsocket


class Bot(AioBot):
    def __init__(self, token: str):

        self.websocket_connection = BotWebsocket(self)

        super().__init__(token)
