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


def get_books_by_id(database : Session, user_id : int, read : int) -> List[String]:
    row = [(x.book, x.rating) for x  in database.query(User).filter(User.user_id == user_id, User.label == read).all()]

    return row


def add_book(database : Session, user_id : int, book : String, read : int) -> bool:
    books = get_books_by_id(database, user_id, read)

    if book in books:
        return False

    database.add(User(user_id=user_id, book=book, label=read, rating=-1)) # -1 == undefined
    database.commit()
    return True


def set_rating(database : Session, user_id : int, book : String, rating : int, read : int) -> bool:
    row = database.query(User).filter(User.user_id==user_id, User.book==book, User.label==read).all()

    if len(row) != 1:
        return False
    
    row[0].rating=rating
    database.commit()

    return True

def remove_book(database : Session, user_id : int, book : String, read : bool) -> bool:
    books = get_books_by_id(database, user_id, read)

    if book not in books:
        return False
    
    database.query(User).filter(User.user_id==user_id, User.book==book, User.label==read).delete()
    database.commit()

    return True




# if __name__ == "__main__":
#     engine = create_engine('sqlite:///database.db', echo=True)

#     Base.metadata.create_all(bind=engine)

#     db = Session(autoflush=False, bind=engine)

#     add_book(db, 1, 'a', 1)
#     # add_book(db, 1, 'b', 1)
#     # add_book(db, 1, 'c', 1)

#     # add_book(db, 1, 'a', 2)
#     # add_book(db, 1, 'b', 2)
#     # add_book(db, 1, 'c', 2)

#     # add_book(db, 2, 'd', 1)
#     # add_book(db, 2, 'e', 1)
#     # add_book(db, 2, 'f', 1)

#     # add_book(db, 2, 'g', 2)
#     # add_book(db, 2, 'h', 2)
#     # add_book(db, 2, 'i', 2)

#     # print(get_books_by_id(db, 1, 13))