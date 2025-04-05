from pydantic import BaseModel
from datetime import date

# Schema cho Phiếu mượn
class BorrowTicketCreate(BaseModel):
    MA_PHIEU: str
    MA_NV: str
    MA_DOC_GIA: str
    DATE_START: date
    DATE_END: date

class BorrowTicketResponse(BaseModel):
    MA_PHIEU: str
    TRANG_THAI: str
    DATE_START: date
    DATE_END: date
    class Config:
        orm_mode = True

# Schema cho Sách
class BookResponse(BaseModel):
    MA_SACH: str
    NAME: str
    GIA_TIEN: int
    class Config:
        orm_mode = True