import sys
import os

# se agrega el path del proyecto al sistema
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog
import requests
import scripts.data_cleaning.data_clean as data_clean

# Configuración de la API
BASE_API_URL = "https://data-migration-globant.onrender.com"
#BASE_API_URL = "http://localhost:8000"

def backup_data():
    
    url = f"{BASE_API_URL}/backup"
    
    try:
        response = requests.post(url)
        if response.status_code == 200:
            messagebox.showinfo("Éxito", f"Backup de completado")
        else:
            messagebox.showerror("Error", f"Fallo en el backup: {response.json()}")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo conectar a la API\n{e}")


def restore_data():
    table_name = entry_table.get().strip()  # Obtener el nombre de la tabla
    if not table_name:
        messagebox.showerror("Error", "Por favor, ingrese un nombre de tabla válido")
        return

    url = f"{BASE_API_URL}/restore/{table_name}"
    
    try:
        response = requests.post(url)
        if response.status_code == 200:
            messagebox.showinfo("Éxito", f"Restauración de {table_name} completada")
        else:
            messagebox.showerror("Error", f"Fallo en la restauración: {response.json()}")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo conectar a la API\n{e}")

def run_migration():
    table_name = entry_table_create.get().strip()  # Obtener el nombre de la tabla
    ruta_archivo= filedialog.askopenfilename(title="Seleccionar archivo", filetypes=(("CSV files", "*.csv"), ("all files", "*.*")))
    
    url = f"{BASE_API_URL}/{table_name}/batch"
    
    try:
        data = data_clean.data_clean(ruta_archivo)  # Aplicar limpieza de datos

        #enviar data a la API
        response = requests.post(url, json={f"{table_name}": data.to_dict(orient="records")})

        if response.status_code == 200:
            messagebox.showinfo("Éxito", "Carga completada correctamente.")
        else:
            messagebox.showerror("Error", f"Falló la carga: {response.text}")
    
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

# Crear la ventana principal
root = tk.Tk()
root.title("Gestión de Migración")
root.geometry("400x300")

# Crear Notebook (pestañas)
notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True, fill="both")

# Pestaña 1: Migración
tab1 = ttk.Frame(notebook)
notebook.add(tab1, text="Creación masiva")

tk.Label(tab1, text="Nombre de la tabla:", font=("Arial", 12)).pack(pady=10)
entry_table_create = tk.Entry(tab1, width=20)
entry_table_create.pack(pady=5)

migrate_label = tk.Label(tab1, text="Migrar datos desde local a la BD (ToDo: desde S3)", font=("Arial", 12))
migrate_label.pack(pady=10)

btn_upload = tk.Button(tab1, text="Seleccionar CSV", command=run_migration, width=20, font=("Arial", 12))
btn_upload.pack(pady=20)

# Pestaña 2: Restauración
tab2 = ttk.Frame(notebook)
notebook.add(tab2, text="Restauración y Backup")

tk.Label(tab2, text="Nombre de la tabla:", font=("Arial", 12)).pack(pady=10)
entry_table = tk.Entry(tab2, width=20)
entry_table.pack(pady=5)

restore_label = tk.Label(tab2, text="Restaurar datos desde backup", font=("Arial", 12))
restore_label.pack(pady=10)

restore_button = tk.Button(tab2, text="Restaurar", command=restore_data, font=("Arial", 12))
restore_button.pack(pady=10)

# Botón para hacer backup
backup_button = tk.Button(tab2, text="Hacer backup de tablas", command=backup_data, font=("Arial", 12))
backup_button.pack(pady=10)

# Ejecutar la aplicación
root.mainloop()
