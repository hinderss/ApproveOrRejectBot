import os
import sys
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from app.database.database import Database
from app.language.lang_setup import Localization

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
dp = Dispatcher(storage=MemoryStorage())
bot = Bot(os.environ.get("BOT_TOKEN"), parse_mode=ParseMode.HTML)
ADMIN_CHAT_ID = os.environ.get("ADMIN_CHAT_ID")
db = Database(os.environ.get("SQLALCHEMY_DATABASE_URI"))
lang = Localization(os.environ.get("LANGUAGES_INI"))

from app.handlers import common, document
dp.include_routers(common.router, document.router)
