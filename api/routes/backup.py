import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from services.backup_avro import export_to_avro, restore_from_avro
from api.config.db_config import SessionLocal
import os

router = APIRouter()

# Dependencia para obtener la sesión de la BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/backup")
def backup_tables(db: Session = Depends(get_db)):
    # se establecen las tablas a respaldar
    tables = ["departments", "jobs", "hired_employees"]
    backup_files = {}
    
    for table in tables:
        try:
            file_path = export_to_avro(table, db)
            backup_files[table] = file_path
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to backup {table}: {str(e)}")
    
    return {"message": "Backup completado, revise la carpeta en el servidor.", "files": backup_files}

@router.post("/restore/{table_name}")
def restore_table(table_name: str, db: Session = Depends(get_db)):
    """API endpoint to restore a table from its AVRO backup."""
    try:
        result = restore_from_avro(table_name, db)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to restore {table_name}: {str(e)}")