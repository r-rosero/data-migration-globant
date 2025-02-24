
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import insert
from sqlalchemy.orm import Session
from api.models.hired_employees import HiredEmployee
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

class Employee(BaseModel):
    id: int
    name: str
    datetime: str
    department_id: int
    job_id: int

class EmployeeBatch(BaseModel):
    employees: List[Employee]

# función encargada de la creación de los jobs
@router.post("/employees")
def create_hired_employee(employee_id: int, employee_name: str, employee_datetime: str, employee_department_id: int, 
                          employee_job_id: int, db: Session = Depends(get_db)):
    new_employee_hired = HiredEmployee(id = employee_id, name = employee_name, datetime = employee_datetime,
                                department_id = employee_department_id, job_id = employee_job_id)
    db.add(new_employee_hired)
    db.commit()
    db.refresh(new_employee_hired)
    return new_employee_hired