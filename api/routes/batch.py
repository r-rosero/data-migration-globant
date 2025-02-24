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

table_map = {
    "employees": HiredEmployee,
    "departments": Department,
    "jobs": Job,
}

@router.post("/batch")
def insert_batch(data: dict, db: Session = Depends(get_db)):
    batch_size = 1000
    total_inserted = 0
    
    try:
        table_name = data.get("table_name")
        records = data.get("records") 

        # Obtener el modelo SQLAlchemy dinámicamente
        model = table_map.get(table_name)
        
        for i in range(0, len(records), batch_size):
            batch = records[i:i + batch_size]
            db.bulk_insert_mappings(model, batch)
            db.commit()
            total_inserted += len(batch)

        return {"mensaje": f"{total_inserted} registros insertados en {table_name}."}
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
