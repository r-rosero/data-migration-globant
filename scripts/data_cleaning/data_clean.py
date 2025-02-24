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

    #validacón de campos nulos
    null_rows = data[data.isnull().any(axis=1)]
    if not null_rows.empty:
        null_rows.to_csv(f"data/migration_logs/{file_name}_nulls.log", index=False)
        data = data.dropna()

    # se valida si existen ids duplicados en el archivo, se elimina y se registra cual id se elimnó en el archivo de log
    duplicate_rows = data[data.duplicated(subset=["id"], keep=False)]
    if not duplicate_rows.empty:
        duplicate_rows.to_csv(f"data/migration_logs/{file_name}_duplicates.log", index=False)
        data = data.drop_duplicates(subset=["id"])

    return data.reset_index(drop=True)