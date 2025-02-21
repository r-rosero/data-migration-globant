
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

@router.post("/departments/batch")
def create_job_batch(batch: DepartmentBatch, db: Session = Depends(get_db)):
    total_inserted = 0
    for depart in batch.departments:
        departments_data = [{"id": depart.id, "department": depart.department}]

        # Si hay más de 1000 registros, dividir en lotes
        for i in range(0, len(departments_data), batch_load_size):
            while departments_data:  # Mientras haya datos en la lista
                data_batch = []  # Creamos un nuevo lote
                for _ in range(min(batch_load_size, len(departments_data))):  # Hasta 1000 elementos
                    data_batch.append(departments_data.pop(0))  # Extraemos de la lista

                db.execute(insert(Department), data_batch)  # Insertamos en la BD
                db.commit()
                total_inserted += len(data_batch)

    return {"mensaje": f"Total registros insertados: {total_inserted}."}