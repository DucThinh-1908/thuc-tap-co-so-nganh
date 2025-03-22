from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from database import get_db
from Services.Users import UserService
from Models.Users import UserCreate, UserUpdate, UserResponse, UserLogin
from typing import List
from sqlalchemy.exc import IntegrityError
from Services.Users import UserService

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if username already exists
    existing_user = UserService.get_user_by_username(db, user.user_name)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    try:
        return UserService.create_user(db, user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error creating user"
        )

@router.get("/", response_model=List[UserResponse])
def read_users(
    skip: int = Query(0, ge=0), 
    limit: int = Query(10, ge=1, le=100), 
    db: Session = Depends(get_db)
):
    return UserService.get_users(db, skip, limit)

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    # Check if username already exists (if username is being updated)
    if user.user_name is not None:
        existing_user = UserService.get_user_by_username(db, user.user_name)
        if existing_user and existing_user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already in use"
            )
    
    updated_user = UserService.update_user(db, user_id, user)
    if updated_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return updated_user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    success = UserService.delete_user(db, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return None

@router.post("/login", response_model=UserLogin, status_code=status.HTTP_201_CREATED)
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    # Check if username already exists
    existing_user = UserService.get_user_by_username(db, user.user_name)
    if existing_user.password == user.password:
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail="User found"
        )
    else: 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
# Các route của readers cần đặt trước route có {user_id}
@router.get("/readers/search")
def find_reader(name: str, db: Session = Depends(get_db)):
    readers = UserService.search_reader(db, name)
    if not readers:
        return {"message": "No readers found with this name"}
    return readers
@router.get("/readers")
def get_readers(db: Session = Depends(get_db)):
    readers = UserService.get_all_readers(db)
    if not readers:
        return {"message": "No readers found"}
    return readers

@router.get("/readers/{reader_id}")
def get_reader(reader_id: str, db: Session = Depends(get_db)):
    reader = UserService.get_reader_by_id(db, reader_id)
    if reader:
        return reader
    return {"message": "Reader not found"}

@router.post("/readers")
def create_reader(reader_data: dict, db: Session = Depends(get_db)):
    try:
        new_reader = UserService.add_reader(db, reader_data)
        return {"message": "Reader created successfully", "reader": new_reader}
    except IntegrityError:
        db.rollback()
        return {"message": "Error creating reader"}

@router.put("/readers/{reader_id}")
def edit_reader(reader_id: str, updated_data: dict, db: Session = Depends(get_db)):
    updated_reader = UserService.update_reader(db, reader_id, updated_data)
    if updated_reader:
        return {"message": "Reader updated successfully", "reader": updated_reader}
    return {"message": "Reader not found"}

@router.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = UserService.get_user(db, user_id)
    if user is None:
        return {"message": "User not found"}
    return user