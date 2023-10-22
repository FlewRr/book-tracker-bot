from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from loader import settings


start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
start_keyboard.row(KeyboardButton(settings.buttons.add), KeyboardButton(settings.buttons.remove))
start_keyboard.row(KeyboardButton(settings.buttons.read), KeyboardButton(settings.buttons.planned))
start_keyboard.add(KeyboardButton(settings.buttons.rate), KeyboardButton(settings.buttons.back))

add_remove_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
add_remove_keyboard.row(KeyboardButton(settings.buttons.read), KeyboardButton(settings.buttons.planned))
add_remove_keyboard.add(KeyboardButton(settings.buttons.back))

yes_no_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
yes_no_keyboard.row(KeyboardButton("Yes"), KeyboardButton("No"))
