import os
import boto3
import fastavro
from sqlalchemy.orm import Session
from sqlalchemy import MetaData, insert, text
from api.config.config_env import S3_BUCKET_NAME, S3_REGION, S3_ACCESS_KEY, S3_SECRET_KEY

s3_client = boto3.client(
    "s3",
    aws_access_key_id=S3_ACCESS_KEY,
    aws_secret_access_key=S3_SECRET_KEY,
    region_name=S3_REGION
)

if os.getenv("RENDER"):
    backup_dir_tmp = "/tmp/backups/"  # Render usa /tmp/ para almacenamiento temporal
    dir_restored_tmp = "/tmp/backups/"
    os.makedirs(dir_restored_tmp, exist_ok=True)
    dir_restored = "/tmp/"
else:
    backup_dir_tmp = "data/backups/"
    dir_restored = "data/"

def get_avro_type(sqlalchemy_type):
    if isinstance(sqlalchemy_type, (int, float)):
        return "int"
    elif isinstance(sqlalchemy_type, bool):
        return "boolean"
    elif isinstance(sqlalchemy_type, str):
        return "string"
    else:
        return "string"

def export_to_avro(table_name: str, db: Session) -> str:
    try:
        # Obtener los datos de la tabla
        query = text(f"SELECT * FROM {table_name}")
        result = db.execute(query)
        columns = result.keys()
        rows = [dict(zip(columns, row)) for row in result.fetchall()]

        if not rows:
            raise Exception("No data found in the table.")

        # Definir el esquema de AVRO con tipos dinámicos
        schema = {
            "type": "record",
            "name": table_name,
            "fields": []
        }

        for col, value in rows[0].items():
            schema["fields"].append({"name": col, "type": ["null", get_avro_type(value)]})

        # Guardar temporalmente en local
        file_path = os.path.join(backup_dir_tmp, f"{table_name}.avro")
        with open(file_path, "wb") as out_file:
            fastavro.writer(out_file, schema, rows)

        # Subir a S3
        s3_key = f"backups/{table_name}.avro"
        s3_client.upload_file(file_path, S3_BUCKET_NAME, s3_key)

        # Eliminar archivo temporal
        os.remove(file_path)

        # Retornar URL de S3
        file_url = f"https://{S3_BUCKET_NAME}.s3.{S3_REGION}.amazonaws.com/{s3_key}"
        return file_url

    except Exception as e:
        raise Exception(f"Error exportando backup de {table_name} a AVRO: {str(e)}")

def restore_from_avro(table_name: str, db: Session):
    try:
        s3_key = f"backups/{table_name}.avro"

        s3_client.download_file(S3_BUCKET_NAME, s3_key, f"{dir_restored}{s3_key}")

        with open(f"{dir_restored}{s3_key}", "rb") as in_file:
            reader = fastavro.reader(in_file)
            rows = [row for row in reader]

        if not rows:
            raise Exception("Archivo de backup vacío.")
        
        metadata = MetaData()
        metadata.reflect(bind=db.get_bind())
        table = metadata.tables[table_name]

        db.execute(text(f"DELETE FROM {table_name}"))
        db.execute(insert(table).values(rows))
        db.commit()

        os.remove(f"{dir_restored}{s3_key}")

        return {"message": f"{len(rows)} registros restaurados a {table_name}."}
    except Exception as e:
        db.rollback()
        raise Exception(f"Error restaurando {table_name}: {str(e)}")