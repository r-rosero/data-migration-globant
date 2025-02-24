from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.config.db_config import SessionLocal
from api.models.departments import Department
from api.models.hired_employees import HiredEmployee
from api.models.jobs import Job
from api.routes.hired_employees import Employee

router = APIRouter()

# Dependencia para obtener la sesión de la BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

TABLES_MAPPING = {
    "employees": HiredEmployee,
    "departments": Department,
    "jobs": Job,
}

@router.post("/batch")
def insert_batch(data: dict, db: Session = Depends(get_db)):
    try:
        table_name = data.get("table_name")  # La tabla a insertar
        records = data.get("records")  # Lista de registros

        if not table_name or not records:
            raise HTTPException(status_code=400, detail="Missing table_name or records")

        # Obtener el modelo SQLAlchemy dinámicamente
        model = TABLES_MAPPING.get(table_name)  
        if not model:
            raise HTTPException(status_code=400, detail=f"Invalid table: {table_name}")

        # Insertar en la tabla correspondiente
        db.bulk_insert_mappings(model, records)
        db.commit()

        return {"message": f"Inserted {len(records)} records into {table_name}."}
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
