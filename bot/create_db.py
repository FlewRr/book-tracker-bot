from database.create_interactions import create_interactions_db, interactions_engine
from database.create_book_storage import create_books_db, books_engine
from mapping_builder import create_mappings
from sqlalchemy.orm import Session
import time
st = time.time()
create_books_db()
create_interactions_db()
print(f'Database was created in {time.time()-st}')
