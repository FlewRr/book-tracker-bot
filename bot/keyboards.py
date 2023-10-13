from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from loader import settings


start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
start_keyboard.row(KeyboardButton(settings.buttons.add), KeyboardButton(settings.buttons.delete))
start_keyboard.row(KeyboardButton(settings.buttons.read), KeyboardButton(settings.buttons.planned))