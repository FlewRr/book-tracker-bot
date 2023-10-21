from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Session
from sqlalchemy import  Column, Integer, String
from typing import List
from sqlalchemy import create_engine


# need to test
    
class Based(DeclarativeBase):
    pass


class Book(Based):
    __tablename__ = 'books_storage'
    id = Column(Integer, primary_key=True)
    book = Column(String)

def add_book_in_storage(database: Session, book: str) -> None:
    rows = database.query(Book).count()
    
    database.add(Book(book=book, id=rows))
    database.commit()

def get_id(database: Session, book: str) -> int:
    row = [x.id for x in database.query(Book).filter(Book.book == book).all()]
    
    return row[0]
    

def get_dict_for_books(database: Session) -> dict[int, str]:
    dict_for_books = {x.id: x.book for x in database.query(Book).all()}

    return dict_for_books

def get_dict_for_ids(database: Session) -> dict[str, int]:
    dict_for_ids = {x.book: x.id for x in database.query(Book).all()}

    return dict_for_ids