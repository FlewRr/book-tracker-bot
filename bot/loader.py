from aiogram import Bot, Dispatcher
from aiogram import types
from aiogram.dispatcher import FSMContext
from settings import BotSettings
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.executor import Executor


settings = BotSettings()
bot = Bot(token=settings.config.token)
dp = Dispatcher(bot, storage=MemoryStorage())

