
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import insert
from sqlalchemy.orm import Session
from api.models.departments import Department
from api.config.db_config import SessionLocal

router = APIRouter()
batch_load_size = 1000

# Dependencia para obtener la sesión de la BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class DepartmentCreate(BaseModel):
    id: int
    department: str

class DepartmentBatch(BaseModel):
    departments: List[DepartmentCreate]

# función encargada de la creación de los jobs
@router.post("/departments")
def create_department(department_id: int, department_name: str, db: Session = Depends(get_db)):
    new_department = Department(id = department_id, department = department_name)
    db.add(new_department)
    db.commit()
    db.refresh(new_department)
    return new_department