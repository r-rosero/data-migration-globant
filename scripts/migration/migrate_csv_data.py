import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import pandas as pd
from api.config.db_config import SessionLocal
from api.models.hired_employees import HiredEmployee
from api.models.jobs import Job
from api.models.departments import Department

def migrate_data_to_db(data, entidad):
    # se crea la sesión de la base de datos
    db = SessionLocal()

    #se cargan los datos leidos y limpiados previamente, en la base de datos
    try:
        match entidad:
            case "jobs":
                for _, job in data.iterrows():
                    db.add(Job(id=job["id"], job=job["job"]))
            
            case "departments":
                for _, department in data.iterrows():
                    db.add(Department(id=department["id"], department=department["department"]))
            
            case "hired_employees":
                for _, hired_employee in data.iterrows():
                    db.add(HiredEmployee(id=hired_employee["id"], name=hired_employee["name"], datetime=hired_employee["datetime"], department_id=hired_employee["department_id"], job_id=hired_employee["job_id"]))
        
        print(entidad)
        db.commit()
        print("Los datos fueron migrados exitosamente a la base de datos de PostgreSQL.")

    except Exception as e:
        db.rollback()
        print(f"Error migrando los datos, se realizó rollback.: {e.args}")
    
    finally:
        db.close()