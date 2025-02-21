import pandas as pd
import os

'''
Función encargada de la limpieza de datos de un archivo csv que se pasa como parámetro.
Para el ejercicio la principal regla es que todos los campos son obligaorios, por lo que si hay un campo en blanco
se eliminará la fila y se enviará al archivo de log ubicado en data/migration_logs.

Adicional también se si hay ids duplicados se eliminará la fila y se enviará al archivo de log.
'''

def data_clean(path_file_csv):

    #cargo el archivo csv
    data = pd.read_csv(path_file_csv)
    file_name = os.path.splitext(os.path.basename(path_file_csv))[0]

    there_are_nulls = False
    there_are_duplicates = False

    #validacón de campos nulos
    for id, row in data.iterrows():
        if row.isnull().values.any():
            there_are_nulls = True
            data.drop(id, inplace=True)
            with open(f"data/migration_logs/{file_name}_nulls.log", "a") as file:
                file.write(f"Se eliminó la fila con id: {id}, por tener valores en nulos.\n")

    if not there_are_nulls:
        with open(f"data/migration_logs/{file_name}_nulls.log", "a") as file:
            file.write(f"Se cargaron todos los registros del archivo.\n")

    # se valida si existen ids duplicados en el archivo, se elimina y se registra cual id se elimnó en el archivo de log
    for id, row in data.iterrows():
        if data.duplicated(subset=["id"]).any():
            there_are_duplicates = True
            data.drop(id, inplace=True)
            with open(f"data/migration_logs/{file_name}_duplicates.log", "a") as file:
                file.write(f"Se eliminó la fila con id: {id}, por tener un id duplicado.\n")

    if not there_are_duplicates:
        with open(f"data/migration_logs/{file_name}_duplicates.log", "a") as file:
            file.write(f"Se cargaron todos los registros del archivo.\n")

    return data