
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.models.jobs import Job
from api.config.db_config import SessionLocal

router = APIRouter(prefix="/jobs", tags=["jobs"])

# Dependencia para obtener la sesión de la BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# función encargada de la creación de los jobs
#Optional[str] = None
@router.post("/")
def create_job(job_id: int, job_name: str, db: Session = Depends(get_db)):
    new_job = Job(id=job_id, job=job_name)
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job
