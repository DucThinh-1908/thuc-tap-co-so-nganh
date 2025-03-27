from sqlalchemy.orm import Session
from sqlalchemy import select
from Models.Pulisher_Author import Publisher, Author
from Models.books import Books, BooksSchema
from typing import List, Optional

class ServiceBooks:
    @staticmethod
    def get_all_books(db: Session):
        readers = db.query(Books).all()  # Trả về danh sách
        return readers

    @staticmethod
    def add_book(db: Session, book: BooksSchema):
    # Kiểm tra Author
        author = db.query(Author).filter(Author.author_id == book.author_id).first()
        if not author:
            raise ValueError(f"Author ID {book.author_id} không tồn tại.")
        
        # Kiểm tra Publisher
        publisher = db.query(Publisher).filter(Publisher.publisher_id == book.publisher_id).first()
        if not publisher:
            raise ValueError(f"Publisher ID {book.publisher_id} không tồn tại.")
        
        # Nếu hợp lệ thì thêm sách
        new_book = Books(**book.dict())
        db.add(new_book)
        db.commit()
        db.refresh(new_book)
        return new_book
    

    @staticmethod
    def update_book(db: Session, book_id, updated_data):
        book = db.query(Books).filter(Books.book_id == book_id).first()
        if not book:
            return None
        allowed_fields = {"name", "quantity", "price", "published_year", "publisher_id", "author_id"}

        # Lọc các trường hợp lệ và không rỗng
        data_to_update = {key: value for key, value in updated_data.items() if key in allowed_fields and value is not None}
        if data_to_update:
            for key, value in data_to_update.items():
                setattr(book, key, value)

            db.commit()
            db.refresh(book)
            return book
        return None

    @staticmethod
    def search_book(db: Session, name: str):
        return db.query(Books).filter(Books.name.ilike(f"%{name}%")).all()
    