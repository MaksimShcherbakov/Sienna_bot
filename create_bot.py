import logging
import os
import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand, BotCommandScopeDefault
from decouple import config
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pywin.scintilla.view import configManager
from sqlalchemy.ext.asyncio import create_async_engine
from aiogram.fsm.storage.redis import RedisStorage
from sqlalchemy.ext.asyncio import async_sessionmaker

from constants import BOT_TOKEN, DATABASE_URL

questions = {
    1: {'qst': 'Столица Италии?', 'answer': 'Рим'},
    2: {'qst': 'Сколько континентов на Земле?', 'answer': 'Семь'},
    3: {'qst': 'Самая длинная река в мире?', 'answer': 'Нил'},
    4: {'qst': 'Какой элемент обозначается символом "O"?', 'answer': 'Кислород'},
    5: {'qst': 'Как зовут главного героя книги "Гарри Поттер"?', 'answer': 'Гарри Поттер'},
    6: {'qst': 'Сколько цветов в радуге?', 'answer': 'Семь'},
    7: {'qst': 'Какая планета третья от Солнца?', 'answer': 'Земля'},
    8: {'qst': 'Кто написал "Войну и мир"?', 'answer': 'Лев Толстой'},
    9: {'qst': 'Что такое H2O?', 'answer': 'Вода'},
    10: {'qst': 'Какой океан самый большой?', 'answer': 'Тихий океан'},
}

engine = create_async_engine(DATABASE_URL, echo=True)

async_session = async_sessionmaker(engine, expire_on_commit=False)

all_media_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'all_media')
scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
admins = [int(admin_id) for admin_id in config('ADMINS').split(',')]

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

storage = RedisStorage.from_url(config('REDIS_URL'))
dp = Dispatcher(storage=storage)
