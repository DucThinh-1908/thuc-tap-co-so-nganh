from sqlalchemy import Column, Integer, String
from database import Base
from pydantic import BaseModel


class Library_staff(Base):
    __tablename__ = "Library_staff"

    id = Column(Integer, primary_key=True,nullable= False)
    name = Column(String(255), nullable=False)
    phone = Column(String(50),nullable=True)
    address = Column(String(255),nullable=True)
class Library_staffSchema(BaseModel):
    id: int
    name: str
    phone: str | None = None
    address: str | None = None

    class Config:
        from_attributes = True