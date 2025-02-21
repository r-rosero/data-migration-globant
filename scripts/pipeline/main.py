import sys
import os

# se agrega el path del proyecto al sistema
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_cleaning.data_clean import data_clean
from migration.migrate_csv_data import migrate_data_to_db

def main(path_file_csv):

    file_name = os.path.splitext(os.path.basename(path_file_csv))[0]

    # Limpieza de datos
    print("Iniciando limpieza de datos...")
    cleaned_data = data_clean(path_file_csv)
    print("Limpieza de datos completada.")

    # Migración de datos
    print("Iniciando migración de datos...")
    migrate_data_to_db(cleaned_data, file_name)
    print("Migración de datos completada.")

if __name__ == "__main__":
    path_file_csv = sys.argv[1]
    main(path_file_csv)