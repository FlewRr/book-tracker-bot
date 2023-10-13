from aiogram import Bot, Dispatcher
from settings import BotSettings
from aiogram.contrib.fsm_storage.memory import MemoryStorage

settings = BotSettings()
bot = Bot(token=settings.token)
dp = Dispatcher(bot, storage=MemoryStorage())