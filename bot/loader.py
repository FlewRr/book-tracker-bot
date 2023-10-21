from aiogram import Bot, Dispatcher
from aiogram import types
from aiogram.dispatcher import FSMContext
from utils.settings import BotSettings
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from database.database import Base
from database.books_db import Based
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from database.create_interactions import create_interactions_db, interactions_engine
from database.create_book_storage import create_books_db, books_engine
from database.books_db import get_dict_for_books
from mapping_builder import create_mappings
import os
import time


st = time.time()

settings = BotSettings()
bot = Bot(token=settings.config.token)
dp = Dispatcher(bot, storage=MemoryStorage())
Base.metadata.create_all(bind=interactions_engine)
db = Session(autoflush=False, bind=interactions_engine)


Based.metadata.create_all(bind=books_engine)
book_storage_db = Session(autoflush=False, bind=books_engine)

fn = time.time()
print(f"EVERYTHING SUCCESSFULLY BUILDED IN {fn-st}")

