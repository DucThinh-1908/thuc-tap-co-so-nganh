from sqlalchemy import Column, Integer, String
from database import Base
from pydantic import BaseModel, Field

class UserModel(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String(100), unique=True, index=True)
    password = Column(String(100))
    role = Column(Integer)

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

class UserResponse(BaseModel):
    id: int
    user_name: str
    password : str
    role: int
    
    class Config:
        from_attributes  = True
