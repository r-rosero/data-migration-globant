from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#string de conexión a la base de datos
database_string = "postgresql://rrosero:rrosero@localhost:5432/data_migration_gl"

# se crea una instancia de motor de base de datos
engine = create_engine(database_string)

# se crea una instancia de sesión de base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)