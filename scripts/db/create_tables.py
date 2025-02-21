import sys
import os

# se agrega el path del proyecto al sistema

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))  # se agrega el path del proyecto al sistema

from api.models.base import Base  # se importa la clase base de los modelos
from api.config.db_config import engine  # se importa la conexión a la base de datos
from api.models.hired_employees import HiredEmployee
from api.models.jobs import Job
from api.models.departments import Department

# se crean todas las tablas en la base de datos relacionadas a la metadata
try:
    print("Conectando con el servidor de base de datos...")
    print("Creando tablas en la base de datos...")
    Base.metadata.create_all(engine)
    print("Las tablas fueron creadas exitosamente.")
except Exception as e:
    print(f"Ocurrió un error al crear las tablas: {e.args}")