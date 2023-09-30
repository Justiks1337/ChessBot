from aiogram import executor

from telegram_log.log import log
from telegram import dp

import telegram_admin
import telegram_authorize
import telegram_dashboard
import telegram_help
import telegram_profile
import telegram_queue
import telegram_start


log.info('bot successful started!')


executor.start_polling(dp, skip_updates=True)
