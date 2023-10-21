from aiogram.utils import executor
from loader import dp     
from handlers import *

if __name__ == "__main__":
    executor.start_polling(dp) 
 