from aiogram.dispatcher.filters.state import State, StatesGroup

class States(StatesGroup):
    add = State()
    remove = State()
    read_list = State()
    planned_list = State()
    