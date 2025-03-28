from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from database import get_db
from Services.statistics import ServiceStatistics

router = APIRouter(prefix="/statistics", tags=["statistics"])

@router.get("/statistics")
def get_statistics(db: Session = Depends(get_db)):
    stats = ServiceStatistics.get_borrow_statistics(db)  # Gọi hàm từ Service
    if not stats:
        return {"message": "No borrow statistics found"}
    return stats