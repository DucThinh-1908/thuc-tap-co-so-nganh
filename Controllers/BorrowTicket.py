from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from Models.Library_staff import models_library_staff
from schemas import schemas

router = APIRouter(prefix="/api/phieu-muon", tags=["Phiếu mượn"])

# Tạo phiếu mượn
@router.post("/", response_model=schemas.BorrowTicketResponse)
def create_phieu_muon(phieu: schemas.BorrowTicketCreate, db: Session = Depends(get_db)):
    # Kiểm tra nhân viên và độc giả
    nv = db.query(models_library_staff.LibraryStaff).filter(models_library_staff.LibraryStaff.MA_NV == phieu.MA_NV).first()
    if not nv:
        raise HTTPException(404, "Nhân viên không tồn tại")
    
    doc_gia = db.query(models_library_staff.Reader).filter(models_library_staff.Reader.MA_DOC_GIA == phieu.MA_DOC_GIA).first()
    if not doc_gia:
        raise HTTPException(404, "Độc giả không tồn tại")
    
    # Tạo phiếu
    new_phieu = models_library_staff.BorrowTicket(
        MA_PHIEU=phieu.MA_PHIEU,
        MA_NV=phieu.MA_NV,
        MA_DOC_GIA=phieu.MA_DOC_GIA,
        DATE_START=phieu.DATE_START,
        DATE_END=phieu.DATE_END,
        TRANG_THAI="ĐANG MƯỢN"
    )
    db.add(new_phieu)
    db.commit()
    return new_phieu

# Thêm sách vào phiếu mượn (Sử dụng stored procedure)
@router.post("/{ma_phieu}/them-sach/{ma_sach}")
def them_sach_vao_phieu(ma_phieu: str, ma_sach: str, db: Session = Depends(get_db)):
    try:
        db.execute(f"EXEC THEM_SACH @p_ticket_id='{ma_phieu}', @p_book_id='{ma_sach}'")
        db.commit()
        return {"message": "Thêm sách thành công"}
    except Exception as e:
        db.rollback()
        raise HTTPException(400, detail=str(e))

# Lấy danh sách phiếu mượn
@router.get("/", response_model=list[schemas.BorrowTicketResponse])
def get_all_phieu(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models_library_staff.BorrowTicket).offset(skip).limit(limit).all()