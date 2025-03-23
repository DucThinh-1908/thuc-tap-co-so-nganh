from sqlalchemy.orm import Session
from sqlalchemy import select
from Models.Books import Books, BooksSchema
from typing import List, Optional

class ServiceBooks:
    @staticmethod
    def get_all_books(db: Session):
        readers = db.query(Books).all()  # Trả về danh sách
        return readers



    @staticmethod
    def add_reader(db: Session, reader_data: BooksSchema):
        new_reader = Books(
            reader_id=reader_data.reader_id,
            name=reader_data.name,
            phone=reader_data.phone,
            address=reader_data.address,
            faculty=reader_data.faculty,
            Class=reader_data.Class
    )
        db.add(new_reader)
        db.commit()
        db.refresh(new_reader)
        return new_reader
    

    @staticmethod
    def update_reader(db: Session, reader_id, updated_data):
        reader = db.query(Books).filter(Books.reader_id == reader_id).first()
        if reader:
            allowed_fields = {"name", "phone", "address", "faculty", "Class"}
        
        # Lọc chỉ những trường hợp lệ
            for key, value in updated_data.items():
                if key in allowed_fields and value is not None:
                    setattr(reader, key, value)
        
            db.commit()  # Lưu thay đổi vào database
            db.refresh(reader)  # Làm mới đối tượng để lấy dữ liệu mới nhất
        
            return reader 
        return None
    

    @staticmethod
    def search_reader(db: Session, name: str):
        return db.query(Readers).filter(Readers.name.ilike(f"%{name}%")).all()
    