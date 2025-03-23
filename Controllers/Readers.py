from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from database import get_db
from Services.Readers import ServiceReaders
from Models.Readers import Readers, ReadersSchema
from typing import List
from sqlalchemy.exc import IntegrityError

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
