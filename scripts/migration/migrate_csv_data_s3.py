from http.client import HTTPException
import os
import boto3
import pandas as pd
from requests import Session
from api.config.config_env import S3_BUCKET_NAME, S3_REGION, S3_ACCESS_KEY, S3_SECRET_KEY

# Configurar acceso a S3
s3_client = boto3.client(
    "s3",
    aws_access_key_id=S3_ACCESS_KEY,
    aws_secret_access_key=S3_SECRET_KEY,
    region_name=S3_REGION
)

tmp_dir_render = "/tmp/data_migration"  # Directorio temporal en Render

# Asegurar que el directorio existe
os.makedirs(tmp_dir_render, exist_ok=True)

def download_csv_from_s3(file_name):
    local_file_path = os.path.join(tmp_dir_render, file_name)
    s3_file_key = f"csv/{file_name}"

    try:
        s3_client.download_file(S3_BUCKET_NAME, s3_file_key, local_file_path)
        print(f"Descargado {file_name} desde S3.")
        return local_file_path
    except Exception as e:
        print(f"Error descargando {file_name}: {str(e)}")
        return None

def load_csv_to_db(file_path: str, model, db: Session):
    try:
        df = pd.read_csv(file_path)
        if df.empty:
            raise HTTPException(status_code=400, detail=f"El archivo {file_path} está vacío.")

        # Convertir DataFrame a diccionarios para bulk_insert
        records = df.to_dict(orient="records")

        # Insertar los datos en la tabla
        db.bulk_insert_mappings(model, records)
        db.commit()
        
        print(f"Datos cargados en {model.__tablename__} desde {file_path}.")
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error en la migración: {str(e)}")
