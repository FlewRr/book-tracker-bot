from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Session
from sqlalchemy import  Column, Integer, String
from typing import List

class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'books'

    user_id = Column(Integer, primary_key=True, index=True)
    read_books = Column(String)
    planned_books = Column(String)


def database_get_by_id(database : Session, user_id : int, read : bool) -> List[String]:
    row = database.get(User, user_id)

    if row == None:
        return None
    else:
        if read:
            return row.read_books.split(';')
        return row.planned_books.split(';')
    

def database_insert(database : Session, user_id : int, book : str, read : bool) -> None:

    row = database.get(User, user_id)

    if row == None:
        if read: 
            database.add(User(user_id=user_id, read_books=book, planned_books=''))
        else:
            database.add(User(user_id=user_id, read_books='', planned_books=book))
        database.commit()
        return
    
    if read:
        row.read_books += ";" + book
    else:
        row.planned_books += ";" + book
    database.commit()


def database_update(database : Session, user_id : int, book : str, read : bool) -> None:

    row = database.get(User, user_id)

    if row == None:
        if read: 
            database.add(User(user_id=user_id, read_books=book, planned_books = ''))
        else:
            database.add(User(user_id=user_id, read_books='', planned_books=book))
        database.commit()
        return

    if read:
        row.read_books = book
    else:
        row.planned_books = book
    database.commit()


def database_remove(database: Session, user_id : int, book : str, read : bool) -> bool:
    
    books = database_get_by_id(database, user_id, read)

    if books == None:
        return False
    
    if book not in books:
        return False
    else:
        books.remove(book)
        database_update(database, user_id, ';'.join(books), read)
        return True 

# Base.metadata.create_all(bind=engine)

# with Session(autoflush=False, bind=engine) as db:
    # database_insert(db, 123, 'Hello', True)
    # database_insert(db, 123, 'DSAMKFASK', False)
    # database_insert(db, 123, 'Bye', True)
    # database_insert(db, 123, 'DSAMKFASdsadK', False)
    # database_insert(db, 123, 'DSAMKFsadssASK', False)
    # database_insert(db, 123, 'Byeasdsa', True)

    # database_remove(db, 123, 'DSAMKFASdsadK', False)
    # database_remove(db, 123, 'Hello', True)
    # database_remove(db, 123, 'DSAMKFsadssASK', False)
    # database_remove(db, 123, 'Byeasdsa', True)
    # print(database_get_by_id(db, 123, True))
    # print(database_get_by_id(db, 123, False))
    # # print(database_get_by_id(db, User, 213445))
    # # print(db.query(User).filter(User.books=='Hello World!').first())