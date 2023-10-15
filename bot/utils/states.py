from aiogram.dispatcher.filters.state import State, StatesGroup

class States(StatesGroup):
    work = State()
    add_read = State()
    add_planned = State()
    remove_read = State()
    remove_planned = State()
    rate_aux = State()
    rate_aux_sec = State()
    rate = State()
    add_choose = State()
    remove_choose = State()
