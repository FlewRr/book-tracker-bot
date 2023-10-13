from aiogram import types
from loader import bot, dp, settings
from aiogram.dispatcher import FSMContext

@dp.message_handler(commands=["start"], state="*")
async def welcome(msg: types.Message, state: FSMContext):
    await msg.reply(settings.messages.welcome)
    