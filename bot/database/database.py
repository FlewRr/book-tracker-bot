from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Session
from sqlalchemy import  Column, Integer, String
from typing import List
from sqlalchemy import create_engine

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    book = Column(String)
    label = Column(Integer) # 1 - read, 2 - planned
    rating = Column(Integer)


def get_all(database: Session):
    rows = database.query(User).all()

    return rows

def get_books_by_id(database : Session, user_id : int, read : int) -> List[String]:
    rows = database.query(User).filter(User.user_id == user_id, User.label == read).all()
    if rows == None:
        return
    row = [(x.book, x.rating) for x in rows]

    return row


def add_book(database : Session, user_id : int, book : str, read : int) -> bool:
    books = [x[0] for x in get_books_by_id(database, user_id, read)]
    rows = database.query(User).count()

    if book in books:
        return False

    database.add(User(id=rows, user_id=user_id, book=book, label=read, rating=-1)) # -1 == undefined
    database.commit()
    return True


def set_rating(database: Session, user_id: int, book: str, rating: int, read: int=1) -> bool:
    row = database.query(User).filter(User.user_id==user_id, User.book==book, User.label==read).all()

    if len(row) != 1:
        return False
    
    row[0].rating=rating
    database.commit()

    return True

def remove_book(database : Session, user_id : int, book : str, read : bool) -> bool:
    books = [x[0] for x in get_books_by_id(database, user_id, read)]
    
    if book not in books:
        return False
    
    database.query(User).filter(User.user_id==user_id, User.book==book, User.label==read).delete()
    database.commit()

    return True



# if __name__ == "__main__":
#     engine = create_engine('sqlite:///database.db', echo=True)
#     Base.metadata.create_all(bind=engine)

#     db = Session(autoflush=False, bind=engine)
    
#     f = pd.read_sql_table('books', con=engine.connect())
#     print(f.head())
    # add_book(db, 1, 'b', 1)
    # add_book(db, 1, 'c', 1)

    # add_book(db, 1, 'a', 2)
    # add_book(db, 1, 'b', 2)
    # add_book(db, 1, 'c', 2)

    # add_book(db, 2, 'd', 1)
    # add_book(db, 2, 'e', 1)
    # add_book(db, 2, 'f', 1)

    # add_book(db, 2, 'g', 2)
    # add_book(db, 2, 'h', 2)
    # add_book(db, 2, 'i', 2)

    # print(get_books_by_id(db, 1, 13))