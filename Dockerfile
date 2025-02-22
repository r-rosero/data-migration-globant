# Usa una imagen de Python
FROM python:3.13

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos al contenedor
COPY . .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto 8000
EXPOSE 8000

# Comando para correr la API
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]