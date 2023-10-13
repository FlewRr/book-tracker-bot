from aiogram import Bot, Dispatcher
from aiogram import types
from aiogram.dispatcher import FSMContext
from utils.settings import BotSettings
from aiogram.contrib.fsm_storage.memory import MemoryStorage


settings = BotSettings()
bot = Bot(token=settings.config.token)
dp = Dispatcher(bot, storage=MemoryStorage())

