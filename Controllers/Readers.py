from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from database import get_db
from Services.Readers import ServiceReaders
from Models.Readers import Readers, ReadersSchema

router = APIRouter(prefix="/readers", tags=["readers"])

@router.get("/readers/search")
def find_reader(name: str, db: Session = Depends(get_db)):
    readers = ServiceReaders.search_reader(db, name)
    if not readers:
        return {"message": "No readers found with this name"}
    return readers


@router.get("/readers")
def get_readers(db: Session = Depends(get_db)):
    readers = ServiceReaders.get_all_readers(db)
    if not readers:
        return {"message": "No readers found"}
    return readers


@router.post("/add")
def add_reader(reader: ReadersSchema, db: Session = Depends(get_db)):
    # Kiểm tra xem độc giả đã tồn tại chưa
    existing_reader = ServiceReaders.search_reader(db, reader.name)
    if existing_reader:
        return {"error": "Already exists"}
    # Thêm độc giả mới
    ServiceReaders.add_reader(db , reader)
    return {"message": "Success"}


@router.put("/readers/{reader_id}")
def edit_reader(reader_id: str, updated_data: dict, db: Session = Depends(get_db)):
    updated_reader = ServiceReaders.update_reader(db, reader_id, updated_data)
    if updated_reader:
        return {"message": "Reader updated successfully", "reader": updated_reader}
    return {"message": "Reader not found"}


@router.delete("/readers/{reader_id}", status_code=status.HTTP_200_OK)
def delete_reader(reader_id: str, db: Session = Depends(get_db)):
    deleted = ServiceReaders.delete_reader(db, reader_id)
    if deleted:
        return {"message": "Reader deleted successfully"}
    raise HTTPException(status_code=404, detail="Reader not found")
