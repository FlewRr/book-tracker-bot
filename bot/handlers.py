from aiogram import types
from loader import dp, settings
from aiogram.dispatcher import FSMContext

@dp.message_handler(commands=["start"], state="*")
async def welcome(message: types.Message, state: FSMContext):
    await message.reply(settings.messages.welcome)
    

@dp.message_handler(commands=['about'])
async def about(message: types.Message):
    await message.reply(settings.messages.about)

@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    await message.reply(settings.messages.help)