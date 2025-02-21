import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from api.config.db_config import SessionLocal
from api.models.hired_employees import HiredEmployee
from api.models.jobs import Job
from api.models.departments import Department

path_data = "data/csv/"

def migrate_data_to_db():
    # se crea la sesión de la base de datos
    db = SessionLocal()

    try:
        # se leen los archivos csv de los datos a migrar que no tienen dependencias
        jobs = pd.read_csv(f"{path_data}jobs.csv")
        departments = pd.read_csv(f"{path_data}departments.csv")

        #casteo de los datos a string para evitar problemas con los datos nulos en la base de datos
        print(jobs["id"].astype(int))

        #se cargan los datos leidos previamente, en la base de datos
        for _, job in jobs.iterrows():
            db.add(Job(id=job["id"], job=job["job"]))

        for _, department in departments.iterrows():
            db.add(Department(id=department["id"], department=department["department"]))
        
        # se leen y cargan los archivos csv de los datos a migrar que tienen dependencias
        hired_employees = pd.read_csv(f"{path_data}hired_employees.csv")

        for _, hired_employee in hired_employees.iterrows():
            db.add(HiredEmployee(id=hired_employee["id"], name=hired_employee["name"], datetime=hired_employee["datetime"], department_id=hired_employee["department_id"], job_id=hired_employee["job_id"]))

        db.commit()
        print("Los datos fueron migrados exitosamente a la base de datos de PostgreSQL.")

    except Exception as e:
        db.rollback()
        print(f"Error migrando los datos, se realizó rollback.: {e}" & e)
    
    finally:
        db.close()

# se ejecuta la función de migración de datos
if __name__ == "__main__":
    migrate_data_to_db()