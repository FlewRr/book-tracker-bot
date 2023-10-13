from aiogram import types
from loader import dp, settings
from aiogram.dispatcher import FSMContext
from utils.states import States
from keyboards import start_keyboard

@dp.message_handler(commands=["start"], state="*")
async def welcome(message: types.Message, state: FSMContext):
    await message.reply(settings.messages.welcome, reply_markup=start_keyboard)
    

@dp.message_handler(commands=['about'], state="*")
async def about(message: types.Message, state: FSMContext):
    await message.reply(settings.messages.about)
    await welcome(message) ##


@dp.message_handler(commands=['help'], state="*")
async def help(message: types.Message, state: FSMContext):
    await message.reply(settings.messages.help)
    await welcome(message) ##


# @dp.message_handler()