import logging
import sys
import asyncio

import create_bot
import database.requests as req

from handlers.start import start_router, questionnaire_router
from aiogram.types import BotCommand, BotCommandScopeDefault
from database.models import async_main


async def set_commands():
    commands = [BotCommand(command='start', description='Старт'),
                BotCommand(command='faq', description='Частые вопросы')]
    await create_bot.bot.set_my_commands(commands, BotCommandScopeDefault())


async def bot_set_commands():
    commands = [BotCommand(command='start', description='Старт'),
                BotCommand(command='registration', description='Регистрация'),
                BotCommand(command='chat_bot', description="Настройки чат-бота")]
    await create_bot.bot.set_my_commands(commands, BotCommandScopeDefault())


async def star_bot():
    await bot_set_commands()
    count_users = await req.get_all_users(count=True)
    try:
        for admin_id in create_bot.admins:
            print(admin_id)
            await create_bot.bot.send_message(admin_id,
                                              f'Бот запущен! Сейчас в базе данных <b>{count_users}</b> пользователей.')
    except:
        pass


async def stop_bot():
    try:
        for admin_id in create_bot.admins:
            await create_bot.bot.send_message(admin_id, 'Бот остановлен 😔')
    except:
        pass


async def main():
    await async_main()

    create_bot.dp.startup.register(star_bot)
    create_bot.dp.shutdown.register(stop_bot)

    create_bot.dp.include_router(start_router)
    create_bot.dp.include_router(questionnaire_router)

    await create_bot.bot.delete_webhook(drop_pending_updates=True)
    await create_bot.dp.start_polling(create_bot.bot)
    await set_commands()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
