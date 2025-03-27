from sqlalchemy import Column, Integer, String
from database import Base
from pydantic import BaseModel


#SQLAlchemy: Quản lý dữ liệu trong database.
#Pydantic: Xác thực và chuyển đổi dữ liệu trong input/output

class Readers(Base):
    __tablename__ = "Readers"

    reader_id = Column(String(255), primary_key=True, nullable=False)
    name = Column(String(255), nullable=False)
    phone = Column(String(15), nullable=True)
    address = Column(String(255), nullable=True)
    faculty = Column(String(255), nullable=True)
    Class = Column(String(50), nullable=True)

class ReadersSchema(BaseModel):
    reader_id: str
    name: str
    phone: str | None = None
    address: str | None = None
    faculty: str | None = None
    Class: str | None = None

    class Config:
        from_attributes = True
