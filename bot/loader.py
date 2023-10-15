from aiogram import Bot, Dispatcher
from aiogram import types
from aiogram.dispatcher import FSMContext
from utils.settings import BotSettings
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from sqlalchemy import create_engine
from database.database import Base
from sqlalchemy.orm import Session

settings = BotSettings()
bot = Bot(token=settings.config.token)
dp = Dispatcher(bot, storage=MemoryStorage())

engine = create_engine('sqlite:///database.db', echo=True)

Base.metadata.create_all(bind=engine)

db = Session(autoflush=False, bind=engine)
