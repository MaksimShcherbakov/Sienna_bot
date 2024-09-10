import psycopg2
import asyncio

from create_bot import bot, dp
from handlers.start import start_router, questionnaire_router
from aiogram.types import BotCommand, BotCommandScopeDefault


from constants import DATABASE_URL

async def set_commands():
    commands = [BotCommand(command='start', description='Старт'),
                BotCommand(command='faq', description='Частые вопросы')]
    await bot.set_my_commands(commands, BotCommandScopeDefault())


async def main():
    # scheduler.add_job(send_time_msg, 'interval', seconds=10)
    # scheduler.start()
    dp.include_router(start_router)
    dp.include_router(questionnaire_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    await set_commands()


if __name__ == "__main__":
    asyncio.run(main())
