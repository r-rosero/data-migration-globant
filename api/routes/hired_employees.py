
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

@router.post("/employees/batch")
def create_hired_employee_batch(batch: EmployeeBatch, db: Session = Depends(get_db)):
    total_inserted = 0

    employees_data = []

    for employee in batch.employees:
        employees_data.append({"id": employee.id, "name": employee.name, "datetime": employee.datetime,
                           "department_id": employee.department_id, "job_id": employee.job_id})

    # Si hay más de 1000 registros, dividir en lotes
    for i in range(0, len(employees_data), batch_load_size):
        data_batch = employees_data[i:i + batch_load_size]
        db.bulk_insert_mappings(Employee, data_batch)
        db.commit()
        total_inserted += len(data_batch)

    return {"mensaje": f"Total registros insertados: {total_inserted}."}