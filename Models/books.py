from sqlalchemy import Column, Integer, String
from database import Base
from pydantic import BaseModel


class Books(Base):
    __tablename__ = "Books"

    book_id = Column(String(255), primary_key=True, nullable=False)
    name = Column(String(255), nullable=False)
    quantity = Column(Integer, nullable=True)
    price = Column(Integer, nullable=True)
    published_year = Column(String(255), nullable=True)
    publisher_id = Column(String(255), nullable=True)
    author_id = Column(String(50), nullable=True)

class BooksSchema(BaseModel):
    book_id: str
    name: str
    quantity: int | None = None
    price: int | None = None
    published_year: str | None = None
    publisher_id: str | None = None
    author_id: str | None = None

    class Config:
        from_attributes = True