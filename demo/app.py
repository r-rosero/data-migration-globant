import tkinter as tk
from tkinter import messagebox
import requests

# Configuración de la API
BASE_API_URL = "https://data-migration-globant.onrender.com"

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

# Configuración de la ventana
root = tk.Tk()
root.title("Gestionador de datos")
root.geometry("350x250")

# Etiqueta y campo de entrada para la tabla
tk.Label(root, text="Nombre de la tabla:", font=("Arial", 12)).pack(pady=10)
entry_table = tk.Entry(root, font=("Arial", 12))
entry_table.pack(pady=5)

# Botón para restaurar
restore_button = tk.Button(root, text="Restaurar Datos", command=restore_data, font=("Arial", 12))
restore_button.pack(pady=20)

# Botón para hacer backup
backup_button = tk.Button(root, text="Hacer backup de tablas", command=backup_data, font=("Arial", 12))
backup_button.pack(pady=10)

# Ejecutar la app
root.mainloop()
