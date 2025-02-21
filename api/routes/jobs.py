from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import insert
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

# función encargada de la creación de los jobs por batch
@router.post("/jobs/batch")
def create_job_batch(batch: JobBatch, db: Session = Depends(get_db)):
    total_inserted = 0
    for job in batch.jobs:
        jobs_data = [{"id": job.id, "job": job.job}]

        # Si hay más de 1000 registros, dividir en lotes
        for i in range(0, len(jobs_data), batch_load_size):
            while jobs_data: 
                data_batch = []
                for _ in range(min(batch_load_size, len(jobs_data))):
                    data_batch.append(jobs_data.pop(0))

                db.execute(insert(Job), data_batch)
                db.commit()
                total_inserted += len(data_batch)

    return {"mensaje": f"Total registros insertados: {total_inserted}."}