from aiogram import Bot as AioBot


class Bot(AioBot):
    def __init__(self, token: str):

        super().__init__(token)
