from sqlalchemy.orm import Session
from sqlalchemy import select
from Models.Library_staff import Library_staff, Library_staffSchema
from Models.Users import UserModel
from Models.statistics import Borrows, Borrows_detail
from typing import List, Optional

class ServiceLibraryStaff:
    @staticmethod
    def get_all_staff(db: Session):
        staff_members = (
            db.query(
                Library_staff.id, 
                Library_staff.name, 
                Library_staff.phone, 
                Library_staff.address,
                UserModel.user_name, 
                UserModel.password, 
                UserModel.role
            )
            .join(UserModel, Library_staff.id == UserModel.id)
            .all()
        )
        
        # Chuyển đổi tuple thành list of dict
        result = []
        for member in staff_members:
            result.append({
                "id": member[0],
                "name": member[1],
                "phone": member[2],
                "address": member[3],
                "user_name": member[4],
                "password": member[5],
                "role": member[6],
            })
        
        return result

    @staticmethod
    def add_staff(db: Session, staff: Library_staffSchema):
        # Tạo bản ghi Library_staff
        new_staff = Library_staff(
            name=staff.name,
            phone=staff.phone,
            address=staff.address
        )
        db.add(new_staff)
        db.commit()
        db.refresh(new_staff)
        
        # Tạo bản ghi User và liên kết với Library_staff
        new_user = UserModel(
            user_name=staff.user.user_name,
            password=staff.user.password,
            role=staff.user.role,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {
            "staff": new_staff,
            "user": new_user
        }
    
    @staticmethod
    def update_staff(db: Session, id: int, updated_data: dict):
        # Lấy thông tin staff và user từ DB
        staff = db.query(Library_staff).filter(Library_staff.id == id).first()
        user = db.query(UserModel).filter(UserModel.id == id).first()

        if not staff or not user:
            return None

        # Các trường cho phép cập nhật
        allowed_staff_fields = {"name", "phone", "address"}
        allowed_user_fields = {"user_name", "password", "role"}

        # Tách dữ liệu
        staff_data = {key: value for key, value in updated_data.items() 
                    if key in allowed_staff_fields and value is not None}

        user_data = updated_data.get("user", {})
        user_data = {key: value for key, value in user_data.items() 
                    if key in allowed_user_fields and value is not None}

        # Cập nhật thông tin bảng Library_staff
        if staff_data:
            for key, value in staff_data.items():
                setattr(staff, key, value)

        # Cập nhật thông tin bảng Users
        if user_data:
            for key, value in user_data.items():
                setattr(user, key, value)

        # Lưu thay đổi
        db.commit()
        db.refresh(staff)
        db.refresh(user)

        return {
            "staff": staff,
            "user": user
        }

    @staticmethod
    def search_staff(db: Session, name: str):
        # ✅ Truy vấn kết hợp hai bảng
        result = (
            db.query(Library_staff, UserModel)
            .join(UserModel, Library_staff.id == UserModel.id)
            .filter(Library_staff.name.ilike(f"%{name}%"))
            .all()
        )

        return [
            {
                "id": staff.id,
                "name": staff.name,
                "phone": staff.phone,
                "address": staff.address,
                "user_name": user.user_name,
                "password" : user.password,
                "role": user.role
            }
            for staff, user in result
        ]
    @staticmethod

    def delete_staff(db: Session, staff_id: int):
        # Lấy danh sách các ticket_id liên quan đến staff_id
        tickets = db.query(Borrows).filter(Borrows.id == staff_id).all()
        
        for ticket in tickets:
            # 1. Xóa Borrow_ticket_detail dựa trên ticket_id (str)
            db.query(Borrows_detail).filter(
                Borrows_detail.ticket_id == ticket.ticket_id
            ).delete()
            
            # 2. Xóa Borrow_ticket dựa trên id (int)
            db.query(Borrows).filter(
                Borrows.id == ticket.id
            ).delete()

        db.query(UserModel).filter(
            UserModel.id == staff_id
        ).delete()

        db.query(Library_staff).filter(
            Library_staff.id == staff_id
        ).delete()
        db.commit()

        return {"message": f"Staff with id {staff_id} has been deleted successfully."}



