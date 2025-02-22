import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.config import get_db
from services.backup_avro import export_to_avro
import os

router = APIRouter()

BACKUP_DIR = "/opt/render/backups"
os.makedirs(BACKUP_DIR, exist_ok=True)

@router.post("/backup")
def backup_tables(db: Session = Depends(get_db)):
    # se establecen las tablas a respaldar
    tables = ["departments", "jobs", "hired_employees"]
    backup_files = {}
    
    for table in tables:
        try:
            file_path = export_to_avro(table & "_" & datetime.now(), db, BACKUP_DIR)
            backup_files[table] = file_path
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to backup {table}: {str(e)}")
    
    return {"message": "Backup completado, revise la carpeta en el servidor.", "files": backup_files}