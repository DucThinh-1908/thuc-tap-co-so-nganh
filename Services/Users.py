from sqlalchemy.orm import Session
from sqlalchemy import select
from Models.Users import UserModel, UserCreate, UserUpdate, UserResponse, UserLogin, Readers
from typing import List, Optional

class UserService:
    
    @staticmethod
    def create_user(db: Session, user: UserCreate) -> UserResponse:
        
        db_user = UserModel(
            user_name=user.user_name,
            password=user.password,
            role=user.role
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        return UserResponse(
            id=db_user.id,
            user_name=db_user.user_name,
            password=db_user.password,
            role=db_user.role
        )
    
    @staticmethod
    def get_users(db: Session, skip: int = 0, limit: int = 10) -> List[UserResponse]:
        users = db.execute(select(UserModel).order_by(UserModel.id).offset(skip).limit(limit)).scalars().all()
        return [
            UserResponse(
                id=user.id,
                user_name=user.user_name,
                password=user.password,
                role=user.role
            ) for user in users
        ]
    
    @staticmethod
    def get_user(db: Session, user_id: int) -> Optional[UserResponse]:
        user = db.get(UserModel, user_id)
        if user is None:
            return None
            
        return UserResponse(
            id=user.id,
            user_name=user.user_name,
            password=user.password,
            role=user.role
        )
    
    @staticmethod
    def get_user_by_username(db: Session, user_name: str) -> Optional[UserModel]:
        return db.query(UserModel).filter(UserModel.user_name == user_name).first()
    
    @staticmethod
    def update_user(db: Session, user_id: int, user_data: UserUpdate) -> Optional[UserResponse]:
        db_user = db.get(UserModel, user_id)
        if db_user is None:
            return None
        
        # Update user fields if provided
        if user_data.user_name is not None:
            db_user.user_name = user_data.user_name
            
        if user_data.password is not None:
            db_user.password = user_data.password
            
        if user_data.role is not None:
            db_user.role = user_data.role
        
        db.commit()
        db.refresh(db_user)
        
        return UserResponse(
            id=db_user.id,
            user_name=db_user.user_name,
            password=db_user.password,
            role=db_user.role
        )
    
    @staticmethod
    def delete_user(db: Session, user_id: int) -> bool:
        db_user = db.get(UserModel, user_id)
        if db_user is None:
            return False
        
        db.delete(db_user)
        db.commit()
        return True
    

    @staticmethod
    def get_all_readers(db: Session):
        readers = db.query(Readers).all()  # Trả về danh sách
        return readers

    

    @staticmethod
    def add_reader(db: Session, reader_data: Readers):
        new_reader = Readers(
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
        reader = db.query(Readers).filter(Readers.reader_id == reader_id).first()
        if reader:
            for key, value in updated_data.items():
                setattr(Readers, key, value)
            db.commit()
            return Readers
        return None
    

    @staticmethod
    def search_reader(db: Session, name: str):
        return db.query(Readers).filter(Readers.name.ilike(f"%{name}%")).all()

