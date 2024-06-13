import asyncio

from telegram_log.log import log
from telegram import dp, bot

import telegram_admin
import telegram_authorize
import telegram_dashboard
import telegram_help
import telegram_profile
import telegram_queue
import telegram_start

from telegram.database_deprecated import Connection


log.info('bot successful started!')


async def main():
    connect = Connection()
    await connect.connect()

    await dp.start_polling(bot)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
