from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from Services.borrow_ticket import ServiceBorrow
from Models.statistics import BorrowsSchema
from typing import List
from datetime import date
from Services import borrow_ticket
from Models.statistics import BorrowsDetailSchema, Borrows

router = APIRouter(prefix="/borrows", tags=["borrows"])

@router.get("/details", response_model=List[BorrowsDetailSchema])
def get_all_details(db: Session = Depends(get_db)):
    return ServiceBorrow.get_all_details(db)

@router.get("/", response_model=List[BorrowsSchema])
def get_all_borrows(db: Session = Depends(get_db)):
    return ServiceBorrow.get_all_tickets(db)

@router.get("/{ticket_id}/details")
def get_borrow_details(ticket_id: str, db: Session = Depends(get_db)):
    details = ServiceBorrow.get_borrow_details(db, ticket_id)
    if not details:
        raise HTTPException(status_code=404, detail="No details found")
    return details

@router.post("/add")
def create_borrow(
    ticket_id: str,
    reader_id: str,
    start_date: date,
    end_date: date,
    book_id: str,
    db: Session = Depends(get_db)
):
    borrow, error = ServiceBorrow.create_borrow(
        db, ticket_id, reader_id, start_date, end_date, book_id
    )
    
    if error:
        raise HTTPException(status_code=400, detail=error)
    
    return borrow

@router.delete("/{ticket_id}")
def delete_borrow(ticket_id: str, db: Session = Depends(get_db)):
    success, error = ServiceBorrow.delete_borrow(db, ticket_id)
    
    if error:
        raise HTTPException(status_code=404, detail=error)
    
    return {"message": "Borrow deleted successfully"}