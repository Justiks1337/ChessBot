from aiogram.filters import Command

from decorators import recharge, in_blacklist, only_in_dm
from authorization_core import send_auth_message
from telegram import dp


@dp.message(Command("authorization"))
@recharge
@only_in_dm
@in_blacklist
async def new_token(message):
    await send_auth_message(message)

