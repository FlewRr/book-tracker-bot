from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from loader import settings


start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
start_keyboard.row(KeyboardButton(settings.buttons.add), KeyboardButton(settings.buttons.remove))
start_keyboard.row(KeyboardButton(settings.buttons.read), KeyboardButton(settings.buttons.planned))
start_keyboard.add(KeyboardButton(settings.buttons.back))

add_mistake_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
add_mistake_keyboard.row(KeyboardButton("Try again :)"), KeyboardButton(settings.buttons.back))

remove_mistake_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
remove_mistake_keyboard.row(KeyboardButton("Try again ;)"), KeyboardButton(settings.buttons.back))


add_remove_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
add_remove_keyboard.row(KeyboardButton(settings.buttons.read), KeyboardButton(settings.buttons.planned))
add_remove_keyboard.add(KeyboardButton(settings.buttons.back))
