import pandas as pd
# from books_db import Based, Book
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

books_engine = create_engine("sqlite:///books.db")

def create_books_db():
    df = pd.read_csv("database/books_data/data.csv", index_col=False)
    books = pd.DataFrame()
    books['book'] = df.title.unique()
    books['id'] = [i for i in range(books.size)]
   
    books.to_sql('books_storage', books_engine, if_exists='replace')

