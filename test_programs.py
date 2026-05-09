from sqlalchemy import create_engine, String, Integer, ForeignKey 
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session

class Base(DeclarativeBase):
    pass

class Library(Base):
    __tablename__ = "library"
    id : Mapped[int] = mapped_column(Integer , primary_key=True)
    name : Mapped[str] = mapped_column(String(50) , nullable= False)
    books : Mapped[list["Book"]] = relationship("Book" , back_populates="library")


class Book(Base):
    __tablename__ = "books"
    id : Mapped[int] = mapped_column(Integer , primary_key= True)
    name : Mapped[str] = mapped_column(String(50) , nullable= False)
    library_id : Mapped[int] = mapped_column(ForeignKey("library.id"))
    library : Mapped["Library"] = relationship("Library" , back_populates="books")


engine = create_engine("sqlite:///warmup.db", echo=True)
Base.metadata.create_all(engine)

with Session(engine) as session :
    library = Library(name ="indian_books")
    session.add(library)
    session.flush()
    book1 = Book(name = "great_india" , library_id = library.id)
    book2 = Book(name = "great_divide" , library_id = library.id)
    session.add(book1)
    session.add(book2)
    session.commit()

with Session(engine) as session :
    book = session.get(Book ,1 )
    print(book.library.name)
    library = session.get(Library , 1 )
    print(library.books)