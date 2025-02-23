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
    backup_dir_tmp = "/tmp/"  # Render usa /tmp/ para almacenamiento temporal
    dir_restored = "tmp/"
else:
    backup_dir_tmp = "data/backups/"
    dir_restored = "data/"

def get_avro_type(sqlalchemy_type):
    """Map SQLAlchemy types to Avro types."""
    if isinstance(sqlalchemy_type, (int, float)):
        return "int"
    elif isinstance(sqlalchemy_type, bool):
        return "boolean"
    elif isinstance(sqlalchemy_type, str):
        return "string"
    else:
        return "string"

def export_to_avro(table_name: str, db: Session) -> str:
    """Exports a table to an AVRO file."""
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

        # Eliminar archivo local después de subirlo (opcional)
        os.remove(file_path)

        # Retornar URL de S3
        file_url = f"https://{S3_BUCKET_NAME}.s3.{S3_REGION}.amazonaws.com/{s3_key}"
        return file_url

    except Exception as e:
        print(f"Error exporting {table_name} to AVRO: {str(e)}")
        raise Exception(f"Error exporting {table_name} to AVRO: {str(e)}")

def restore_from_avro(table_name: str, db: Session):
    """Restores data from an AVRO backup file into the database."""
    try:
        s3_key = f"backups/{table_name}.avro"

        s3_client.download_file(S3_BUCKET_NAME, s3_key, f"{dir_restored}{s3_key}")
        
        if not os.path.exists(f"{backup_dir_tmp}/{table_name}.avro"):
            raise Exception("Backup file not found.")

        with open(f"{backup_dir_tmp}{table_name}.avro", "rb") as in_file:
            reader = fastavro.reader(in_file)
            rows = [row for row in reader]

        if not rows:
            raise Exception("No data found in backup file.")
        
        metadata = MetaData()
        metadata.reflect(bind=db.get_bind())
        table = metadata.tables[table_name]

        db.execute(text(f"DELETE FROM {table_name}"))
        db.execute(insert(table).values(rows))
        db.commit()

        os.remove(f"data/{s3_key}")

        return {"message": f"Successfully restored {len(rows)} records to {table_name}."}
    except Exception as e:
        db.rollback()
        raise Exception(f"Error restoring {table_name} from AVRO: {str(e)}")