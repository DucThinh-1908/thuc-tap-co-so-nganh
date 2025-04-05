from sqlalchemy import Column, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class BorrowTicket(Base):
    __tablename__ = "Borrow_ticket"
class BorrowTicket(Base):
    __tablename__ = "disach_phieu_muon"
    MA_PHIEU = Column(String, primary_key=True)
    MA_NV = Column(String, ForeignKey("disach_nhan_vien_thu_vien.MA_NV"))
    MA_DOC_GIA = Column(String, ForeignKey("disach_doc_gia.MA_DOC_GIA"))
    DATE_START = Column(Date)
    DATE_END = Column(Date)
    TRANG_THAI = Column(String)
    staff = relationship("LibraryStaff")
    reader = relationship("Reader")

# Chi tiết phiếu mượn
class BorrowDetail(Base):
    __tablename__ = "disach_phieu_muon_sach"
    MA_PHIEU = Column(String, ForeignKey("disach_phieu_muon.MA_PHIEU"), primary_key=True)
    MA_SACH = Column(String, ForeignKey("disach_sach.MA_SACH"), primary_key=True)
