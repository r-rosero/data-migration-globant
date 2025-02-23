import os
import boto3
import fastavro
from sqlalchemy.orm import Session
from sqlalchemy import text

# Configuración de S3
S3_BUCKET_NAME = "data-migration-globant"
S3_REGION = "us-east-2"
S3_ACCESS_KEY = "AKIAU5LH6BM3FCHPAOII"
S3_SECRET_KEY = "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"

s3_client = boto3.client(
    "s3",
    aws_access_key_id=S3_ACCESS_KEY,
    aws_secret_access_key=S3_SECRET_KEY,
    region_name=S3_REGION
)

def get_avro_type(sqlalchemy_type):
    """Map SQLAlchemy types to Avro types."""
    if isinstance(sqlalchemy_type, (int, float)):
        return "int"
    elif isinstance(sqlalchemy_type, bool):
        return "boolean"
    elif isinstance(sqlalchemy_type, str):
        return "string"
    else:
        return "string"  # Default fallback

def export_to_avro(table_name: str, db: Session) -> str:
    backup_dir="data/backups"
    
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
            print(get_avro_type)
            schema["fields"].append({"name": col, "type": ["null", get_avro_type(value)]})


        # Guardar temporalmente en local
        file_path = os.path.join(backup_dir, f"{table_name}.avro")
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