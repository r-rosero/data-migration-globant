from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#string de conexión a la base de datos
database_string = "postgresql://neondb_owner:npg_mFvikogf8jN5@ep-purple-shadow-a5z8xnwj-pooler.us-east-2.aws.neon.tech/data_migration_gl?sslmode=require"

# se crea una instancia de motor de base de datos
engine = create_engine(database_string, echo=True)

# se crea una instancia de sesión de base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)