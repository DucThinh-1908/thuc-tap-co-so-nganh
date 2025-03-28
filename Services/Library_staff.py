from sqlalchemy.orm import Session
from sqlalchemy import select
from Models.Library_staff import Library_staff, Library_staffSchema
from typing import List, Optional

class ServiceLibraryStaff:
    @staticmethod
    def get_all_staff(db: Session):
        staff_members = db.query(Library_staff).all()  
        return staff_members

    @staticmethod
    def add_staff(db: Session, staff: Library_staffSchema):
        # Tạo đối tượng LibraryStaff từ dữ liệu xác thực
        new_staff = Library_staff(**staff.dict())
        db.add(new_staff) 
        db.commit()  
        db.refresh(new_staff) 
        return new_staff

    @staticmethod
    def update_staff(db: Session, staff_id: int, updated_data: dict):
        staff = db.query(Library_staff).filter(Library_staff.id == staff_id).first()  
        if not staff:
            return None  
        allowed_fields = {"name", "phone", "address"} 
        # Lọc các trường hợp hợp lệ và không phải `None`
        data_to_update = {key: value for key, value in updated_data.items() if key in allowed_fields and value is not None}
        if data_to_update:
            for key, value in data_to_update.items():
                setattr(staff, key, value)
            db.commit()
            db.refresh(staff)
            return staff
        return None

    @staticmethod
    def search_staff(db: Session, name: str):
        return db.query(Library_staff).filter(Library_staff.name.ilike(f"%{name}%")).all() 
