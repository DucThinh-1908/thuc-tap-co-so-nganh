from sqlalchemy import Column, Integer, String
from database import Base
from pydantic import BaseModel, Field

class UserModel(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    user_name = Column(String(100), unique=True, index=True)
    password = Column(String(100))
    role = Column(Integer)

class UserSchema(BaseModel):
    user_name: str
    password: str
    role: int

# Pydantic models for data validation
class UserCreate(BaseModel):
    user_name: str
    password: str
    role: int

class UserUpdate(BaseModel):
    user_name: str = None
    password: str = None
    role: int = None

class UserLogin(BaseModel):
    user_name: str
    password: str

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Readers(Base):
    __tablename__ = "Readers"

    reader_id = Column(String(255), primary_key=True, nullable=False)
    name = Column(String(255), nullable=False)
    faculty = Column(String(255), nullable=True)
    Class = Column(String(50), nullable=True)
    address = Column(String(255), nullable=True)
    phone = Column(String(15), nullable=True)

class ReadersSchema(BaseModel):
    reader_id: str
    name: str
    faculty: str | None = None
    Class: str | None = None
    address: str | None = None
    phone: str | None = None

    class Config:
        from_attributes = True
class UserResponse(BaseModel):
    id: int
    user_name: str
    password : str
    role: int
    
    class Config:
        from_attributes  = True
