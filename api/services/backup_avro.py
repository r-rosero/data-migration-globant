import os
import fastavro
from sqlalchemy.orm import Session
from sqlalchemy import text

def export_to_avro(table_name: str, db: Session, backup_dir: str) -> str:
    """Exports a table from PostgreSQL to an AVRO file."""
    file_path = os.path.join(backup_dir, f"{table_name}.avro")
    
    try:
        query = text(f"SELECT * FROM {table_name}")
        result = db.execute(query)
        columns = result.keys()
        records = [dict(zip(columns, row)) for row in result]
        
        schema = {
            "type": "record",
            "name": table_name,
            "fields": [{"name": col, "type": ["null", "string"]} for col in columns]
        }
        
        with open(file_path, "wb") as avro_file:
            fastavro.writer(avro_file, schema, records)
        
        return file_path
    except Exception as e:
        raise Exception(f"Error exporting {table_name} to AVRO: {str(e)}")