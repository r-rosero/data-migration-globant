from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from api.config.db_config import SessionLocal
from api.models.departments import Department
from api.models.hired_employees import HiredEmployee
from api.models.jobs import Job
from scripts.migration.migrate_csv_data_s3 import download_csv_from_s3, load_csv_to_db 

router = APIRouter()

# Dependencia para obtener la sesión de la BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Mapeo de archivos CSV a modelos SQLAlchemy
csv_files = {
    "departments.csv": (Department, "departments"),
    "jobs.csv": (Job, "jobs"),
    "hired_employees.csv": (HiredEmployee, "hired_employees"),
}

@router.post("/migrate")
def migrate_data(db: Session = Depends(get_db)):
    """Endpoint para migrar datos desde archivos CSV almacenados en S3 a la base de datos."""
    try:
        for file_name, (model, table_name) in csv_files.items():
            local_file = download_csv_from_s3(file_name)
            if local_file:
                load_csv_to_db(local_file, model, db)

        return {"message": "Migración completada exitosamente desde S3."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la migración: {str(e)}")