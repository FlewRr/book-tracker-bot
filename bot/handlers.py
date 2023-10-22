from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp, settings, db, book_storage_db, interactions_engine, create_mappings
from utils.states import States
from keyboards import start_keyboard, add_mistake_keyboard, remove_mistake_keyboard, add_remove_keyboard
from database.database import get_books_by_id, add_book, set_rating, remove_book
from database.books_db import get_dict_for_books, add_book_in_storage
from annoy_builder import get_recs_for_user, build_annoy

dict_for_books = get_dict_for_books(book_storage_db)

@dp.message_handler(commands=["start"], state="*")
async def welcome(message: types.Message, state: FSMContext):
    await States.work.set()
    await message.answer(settings.messages.welcome, reply_markup=start_keyboard)
    

@dp.message_handler(commands=['about'], state="*")
async def about(message: types.Message, state: FSMContext):
    await message.answer(settings.messages.about)
    await welcome(message, state)


@dp.message_handler(commands=['help'], state="*")
async def help(message: types.Message, state: FSMContext):
    await message.answer(settings.messages.help)
    await welcome(message, state)

@dp.message_handler(commands=['recs'], state="*")
async def recs(message: types.Message, state: FSMContext):
    read_books = get_books_by_id(database=db, user_id=message.from_user.id, read=1)
    planned_books = get_books_by_id(database=db, user_id=message.from_user.id, read=2)

    if len(read_books) == 0 and len(planned_books) == 0:
        await message.answer("You have no books in the lists. Add them and try again later.")
        await welcome(message, state)
    else:
        await message.answer('Recommendations has started to be generated. Please, wait. :)')
        create_mappings(interactions_engine, "books", book_storage_db)

        ann = build_annoy()
        recs = [dict_for_books[x] for x in get_recs_for_user(ann, message.from_user.id, [])]
        await message.answer(('\n'.join([str(x) for x in recs])).strip())
        await welcome(message, state)            

@dp.message_handler(state=States.work)
async def start(message: types.Message, state):
    if message.text == settings.buttons.add or message.text == 'Try again :)':
        await States.add_choose.set()
        await message.answer("Where would you like your book to be added in? Read or planned?",  reply_markup=add_remove_keyboard)
    elif message.text == settings.buttons.remove or message.text == 'Try again ;)':
        await States.remove_choose.set()
        await message.answer("Where should I delete the book from? From read or planned?",  reply_markup=add_remove_keyboard)
    elif message.text == settings.buttons.read:
        read_books = get_books_by_id(database=db, user_id=message.from_user.id, read=1)
        if len(read_books) == 0:
            await message.answer("There is none books in your read list. Add them and come back later :)")
            await welcome(message, state)
        else:
            await message.answer(('\n'.join([str(x[0]) + " : " + str(x[1]) for x in read_books])).strip())
            await welcome(message, state) 
    elif message.text == settings.buttons.planned:
        planned_books = get_books_by_id(database=db, user_id=message.from_user.id, read=2)
        if len(planned_books) == 0:
            await message.answer("There is none books in your list. Add them and come back later :)")
            await welcome(message, state)
        else:
            await message.answer(('\n'.join([str(x[0]) + " : " + str(x[1]) for x in planned_books])).strip())            
            await welcome(message, state) 
    elif message.text == settings.buttons.rate:
        await States.rate_aux.set()
        await message.answer("Send me the name of the book you'd like to rate? o_o")
    elif message.text == settings.buttons.back:
        await message.answer(settings.messages.off)
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
    
    f = add_book(database=db, user_id=message.from_user.id, book=message.text, read=1)
    if not f:
        await message.answer("Oops, I guess this book is already in the list. Try again.")
        await welcome(message, state)
    else:
        add_book_in_storage(database=book_storage_db, book=message.text)
        await message.answer("The book has been added to read books.")
        await welcome(message, state)


@dp.message_handler(state=States.add_planned)
async def add_book_to_planned(message: types.Message, state: FSMContext):

    if message.text == settings.buttons.back:
        await welcome(message, state)
        return 0

    f = add_book(database=db, user_id=message.from_user.id, book=message.text, read=2)

    if not f:
        await message.answer("Oops, I guess this book is already in the list. Try again.")
        await welcome(message, state)
    else:
        add_book_in_storage(database=book_storage_db, book=message.text)
        await message.answer("The book has been added to read books.")
        await welcome(message, state)


@dp.message_handler(state=States.remove_read)
async def remove_book_from_read(message: types.Message, state: FSMContext):

    if message.text == settings.buttons.back:
        await welcome(message, state)
        return 0
    
    f = remove_book(database=db, user_id=message.from_user.id, book=message.text, read=1)
    if not f:
        await message.answer("Oops, there is no such a book in your list. Try again.")
        await welcome(message, state)
    else:
        await message.answer("The book has been removed from the read books.")
        await welcome(message, state)


@dp.message_handler(state=States.remove_planned)
async def remove_book_from_planned(message: types.Message, state: FSMContext):

    if message.text == settings.buttons.back:
        await welcome(message, state)
        return 0
    
    f = remove_book(database=db, user_id=message.from_user.id, book=message.text, read=2)
    
    if not f:
        await message.answer("Oops, there is no such a book in your list. Try again.")
        await welcome(message, state)
    else:
        await message.answer("The book has been removed from the read books.")
        await welcome(message, state)

@dp.message_handler(state=States.rate_aux)
async def rate_aux(message: types.Message, state: FSMContext):
    global book
    book = message.text
    
    await States.rate.set()
    await message.answer("Give me the number from 0 to 5, that'll be the rating of the book.")


@dp.message_handler(state=States.rate)
async def rate(message: types.Message, state: FSMContext):
    try:
        rating = int(message.text)
        if rating >= 0 and rating <=5:
            f = set_rating(db, message.from_user.id, book, message.text)

            if f:
                await message.answer("The rating was set successfully")
            else:
                await message.answer("Something gone wrong. Try again.")

            await welcome(message, state)
        else:
            await message.answer("Rating must be number from 0 to 5!")
            await welcome(message, state)
    except:
        await message.answer("Rating must be number from 1 to 10!")
        await welcome(message, state)
