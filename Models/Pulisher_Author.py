from sqlalchemy import Column, Integer, String
from database import Base
from pydantic import BaseModel

class Publisher(Base):
    __tablename__ = "Publisher"

    publisher_id = Column(String(255), primary_key=True, nullable=False)
    name = Column(String(255), nullable=False)

class PublishersSchema(BaseModel):
    publisher_id: str
    name: str

    class Config:
        from_attributes = True

class Author(Base):
    __tablename__ = "Author"

    author_id = Column(String(255), primary_key=True, nullable=False)
    name = Column(String(255), nullable=False)

class AuthorSchema(BaseModel):
    author_id: str
    name: str

    class Config:
        from_attributes = True