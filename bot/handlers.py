from aiogram import types
from loader import dp, settings
from aiogram.dispatcher import FSMContext
from utils.states import States
from keyboards import start_keyboard, add_mistake_keyboard, remove_mistake_keyboard, add_remove_keyboard

read_books = []
planned_books = []


@dp.message_handler(commands=["start"], state="*")
async def welcome(message: types.Message, state: FSMContext):
    await States.work.set()
    await message.answer(settings.messages.welcome, reply_markup=start_keyboard)
    

@dp.message_handler(commands=['about'], state="*")
async def about(message: types.Message, state: FSMContext):
    await message.answer(settings.messages.about)
    await welcome(message, state) ##


@dp.message_handler(commands=['help'], state="*")
async def help(message: types.Message, state: FSMContext):
    await message.answer(settings.messages.help)
    await welcome(message, state) ##


@dp.message_handler(state=States.work)
async def start(message: types.Message, state):
    if message.text == settings.buttons.add or message.text == 'Try again :)':
        await States.add_choose.set()
        await message.answer("Where would you like to be your book added in? Read or planned?",  reply_markup=add_remove_keyboard)
    elif message.text == settings.buttons.remove or message.text == 'Try again ;)':
        await States.remove_choose.set()
        await message.answer("Where would you like to be your book added in? Read or planned?",  reply_markup=add_remove_keyboard)
    elif message.text == settings.buttons.read:
        await message.answer(' '.join(read_books))
        await welcome(message, state) 
    elif message.text == settings.buttons.planned:
        await message.answer(' '.join(planned_books))
        await welcome(message, state) 
    elif message.text == settings.buttons.back:
        return 0
    

@dp.message_handler(state=States.remove_choose)
async def remove_choose(message: types.Message, state: FSMContext):
    if message.text == 'read':
        await States.remove_read.set()
        await message.answer(settings.messages.remove)
    elif message.text == 'planned':
        await States.remove_planned.set()
        await message.answer(settings.messages.remove)
    else:
        await message.answer("I don't get it. Try again.")
        await welcome(message, state)

@dp.message_handler(state=States.add_choose)
async def add_choose(message: types.Message, state: FSMContext):
    if message.text == 'read':
        await States.add_read.set()
        await message.answer(settings.messages.add)
    elif message.text == 'planned':
        await States.add_planned.set()
        await message.answer(settings.messages.add)
    else:
        await message.answer("I don't get it. Try again.")
        await welcome(message, state)


@dp.message_handler(state=States.add_read)
async def add_book_to_read(message: types.Message, state: FSMContext):
    book = ''.join([x.lower() for x in message.text])
    if book in read_books:
        await message.answer("Oops, I guess this book is already in the list. Try again.")
        await add_choose(message, state)
    else:
        read_books.append(book)
        await message.answer("The book has been added to read books.")
        await welcome(message, state)
        print(read_books)

@dp.message_handler(state=States.add_planned)
async def add_book_to_planned(message: types.Message, state: FSMContext):
    book = ''.join([x.lower() for x in message.text])
    if book in read_books:
        await message.answer("Oops, I guess this book is already in the list. Try again.")
        await add_choose(message, state)
    else:
        planned_books.append(book)
        await message.answer("The book has been added to planned.")
        await welcome(message, state)
        print(planned_books)


@dp.message_handler(state=States.remove_read)
async def remove_book_from_read(message: types.Message, state: FSMContext):
    book = ''.join([x.lower() for x in message.text])
    if book not in read_books:
        await message.answer("Oops, there is no such a book in your list. Try again.")
        await remove_choose(message, state)
    else:
        read_books.remove(book)
        await message.answer("The book has been removed from the read books.")
        await welcome(message, state)
        print(read_books)


@dp.message_handler(state=States.remove_planned)
async def remove_book_from_planned(message: types.Message, state: FSMContext):
    book = ''.join([x.lower() for x in message.text])
    if book not in planned_books:
        await message.answer("Oops, there is no such a book in your list. Try again.")
        await remove_choose(message, state)
    else:
        planned_books.remove(book)
        await message.answer("The book has been removed from planned.")
        await welcome(message, state)
        print(planned_books)
