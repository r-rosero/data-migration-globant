
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.models.departments import Department
from api.config.db_config import SessionLocal

router = APIRouter(prefix="/departments", tags=["departments"])

# Dependencia para obtener la sesión de la BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# función encargada de la creación de los jobs
@router.post("/")
def create_department(department_id: int, department_name: str, db: Session = Depends(get_db)):
    new_department = Department(id = department_id, job = department_name)
    db.add(new_department)
    db.commit()
    db.refresh(new_department)
    return new_department