from aiogram import types
from loader import dp, settings, db
from aiogram.dispatcher import FSMContext
from utils.states import States
from keyboards import start_keyboard, add_mistake_keyboard, remove_mistake_keyboard, add_remove_keyboard
from database.db import database_get_by_id, database_insert, database_remove, database_update

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
        await message.answer("Where would you like your book to be added in? Read or planned?",  reply_markup=add_remove_keyboard)
    elif message.text == settings.buttons.remove or message.text == 'Try again ;)':
        await States.remove_choose.set()
        await message.answer("Where should I delete the book from? From read or planned?",  reply_markup=add_remove_keyboard)
    elif message.text == settings.buttons.read:
        read_books = database_get_by_id(database=db, user_id=message.from_user.id, read=True)
        if read_books == None or read_books=='' or len(read_books) == 1:
            await message.answer("There is none books in your read list. Add them and come back later :)")
            await welcome(message, state)
        else:
            await message.answer(('\n'.join(read_books)).strip())
            await welcome(message, state) 
    elif message.text == settings.buttons.planned:
        planned_books = database_get_by_id(database=db, user_id=message.from_user.id, read=False)
        if planned_books == None or len(planned_books)==1:
            await message.answer("There is none books in your list. Add them and come back later :)")
            await welcome(message, state)
        else:
            await message.answer(('\n'.join(planned_books)).strip())
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
    elif message.text == settings.buttons.back:
        await welcome(message, state)
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
    elif message.text == settings.buttons.back:
        await welcome(message, state)
    else:
        await message.answer("I don't get it. Try again.")
        await welcome(message, state)


@dp.message_handler(state=States.add_read)
async def add_book_to_read(message: types.Message, state: FSMContext):

    if message.text == settings.buttons.back:
        await welcome(message, state)
        return 0
    
    book = message.text
    books = database_get_by_id(database=db, user_id=message.from_user.id, read=True)
    if books != None and books != None and book in books:
        await message.answer("Oops, I guess this book is already in the list. Try again.")
        await welcome(message, state)
    else:
        database_insert(database=db, user_id=message.from_user.id, book=book, read=True)
        await message.answer("The book has been added to read books.")
        await welcome(message, state)


@dp.message_handler(state=States.add_planned)
async def add_book_to_planned(message: types.Message, state: FSMContext):

    if message.text == settings.buttons.back:
        await welcome(message, state)
        return 0
    
    book = message.text
    books = database_get_by_id(database=db, user_id=message.from_user.id, read=False)
    if books != None and book in books:
        await message.answer("Oops, I guess this book is already in the list. Try again.")
        await welcome(message, state)
    else:
        database_insert(database=db, user_id=message.from_user.id, book=book, read=False)
        await message.answer("The book has been added to planned.")
        await welcome(message, state)


@dp.message_handler(state=States.remove_read)
async def remove_book_from_read(message: types.Message, state: FSMContext):

    if message.text == settings.buttons.back:
        await welcome(message, state)
        return 0
    
    book = message.text
    books = database_get_by_id(database=db, user_id=message.from_user.id, read=True)
    if books != None and book not in books:
        await message.answer("Oops, there is no such a book in your list. Try again.")
        await welcome(message, state)
    else:
        database_remove(database=db, user_id=message.from_user.id, book=book, read=True)
        await message.answer("The book has been removed from the read books.")
        await welcome(message, state)


@dp.message_handler(state=States.remove_planned)
async def remove_book_from_planned(message: types.Message, state: FSMContext):

    if message.text == settings.buttons.back:
        await welcome(message, state)
        return 0
    
    book = message.text
    books = database_get_by_id(database=db, user_id=message.from_user.id, read=False)
    if book not in books:
        await message.answer("Oops, there is no such a book in your list. Try again.")
        await welcome(message, state)
    else:
        database_remove(database=db, user_id=message.from_user.id, book=book, read=False)
        await message.answer("The book has been removed from planned.")
        await welcome(message, state)
