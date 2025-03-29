from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from Services.Library_staff import ServiceLibraryStaff
from Models.Library_staff import Library_staff, Library_staffSchema
from typing import List
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/staff", tags=["staff"])

@router.get("/staff/search")
def search_staff(name: str, db: Session = Depends(get_db)):
    staff = ServiceLibraryStaff.search_staff(db, name)
    if not staff:
        return {"message": "No staff found with this name"}
    return staff


@router.get("/staff")
def get_all_staff(db: Session = Depends(get_db)):
    staff = ServiceLibraryStaff.get_all_staff(db)
    if not staff:
        return {"message": "No staff found"}
    return staff


@router.post("/add")
def add_staff(staff: Library_staffSchema, db: Session = Depends(get_db)):
    try:
        return ServiceLibraryStaff.add_staff(db, staff)
    except ValueError as e:
        return {"error": str(e)}


@router.put("/staff/{id}")
def update_staff(staff_id: int, updated_data: dict, db: Session = Depends(get_db)):
    updated_staff = ServiceLibraryStaff.update_staff(db, staff_id, updated_data)
    if updated_staff:
        return {"message": "Staff updated successfully", "staff": updated_staff}
    return {"message": "Staff not found"}


@router.delete("/staff/{staff_id}")
def delete_staff(staff_id: int, db: Session = Depends(get_db)):
    return ServiceLibraryStaff.delete_staff(db, staff_id)
