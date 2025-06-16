from sqlalchemy import Column, Integer, String, Date
from database import Base
from pydantic import BaseModel
from datetime import date


class Borrows(Base):
    __tablename__ = "Borrow_ticket"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(String(255), nullable=False)
    reader_id = Column(String(255), nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    status = Column(String(255), nullable=True)

class BorrowsSchema(BaseModel):
    id: int
    ticket_id: str
    reader_id: str
    start_date: date | None = None
    end_date: date | None = None
    status: str | None = None

    class Config:
        from_attributes = True


class Borrows_detail(Base):
    __tablename__ = "Borrow_ticket_detail"

    ticket_id = Column(String(255), primary_key=True, nullable=False)
    book_id = Column(String(255), primary_key=True, nullable=True)

class BorrowsDetailSchema(BaseModel):

    ticket_id: str
    book_id: str

    class Config:
        from_attributes = True


class BorrowRequest(BaseModel):
    ticket_id: str
    reader_id: str
    start_date: date
    end_date: date
    book_id: str