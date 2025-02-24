from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.models.jobs import Job, JobBatch
from api.config.db_config import SessionLocal
from pydantic import BaseModel

router = APIRouter()
batch_load_size = 1000

# Dependencia para obtener la sesión de la BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class JobCreate(BaseModel):
    id: int
    job: str

class JobBatch(BaseModel):
    jobs: List[JobCreate]

# función encargada de la creación de los jobs individuales
#Optional[str] = None
@router.post("/jobs")
def create_job(job_id: int, job_name: str, db: Session = Depends(get_db)):
    new_job = Job(id=job_id, job=job_name)
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job