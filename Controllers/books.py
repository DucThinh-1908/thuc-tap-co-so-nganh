from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from database import get_db
from Services.books import ServiceBooks
from Models.Books import Books, BooksSchema
from typing import List
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/books", tags=["books"])

@router.get("/books/search")
def find_reader(name: str, db: Session = Depends(get_db)):
    books = ServiceBooks.search_book(db, name)
    if not books:
        return {"message": "No readers found with this name"}
    return books


@router.get("/books")
def get_books(db: Session = Depends(get_db)):
    books = ServiceBooks.get_all_books(db)
    if not books:
        return {"message": "No readers found"}
    return books


@router.post("/add")
def add_book(book: BooksSchema, db: Session = Depends(get_db)):
    try:
        return ServiceBooks.add_book(db, book)
    except ValueError as e:
        return {"error": str(e)}


@router.put("/books/{book_id}")
def edit_book(book_id: str, updated_data: dict, db: Session = Depends(get_db)):
    updated_book = ServiceBooks.update_book(db, book_id, updated_data)
    if updated_book:
        return {"message": "Reader updated successfully", "reader": updated_book}
    return {"message": "Reader not found"}
