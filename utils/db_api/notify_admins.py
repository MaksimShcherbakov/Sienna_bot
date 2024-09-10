import logging

from aiogram import Dispatcher

from constants import ADMIN_IDS

async def on_startup_notify(dp: Dispatcher):
    for admin in ADMIN_IDS:
        try:
            text = 'Бот запущен...'
            await dp.bot.send_message(admin, text)
        except Exception as err:
            logging.exception(err)
