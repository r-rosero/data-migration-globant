# data-migration-globant

## Overview
Este proyecto es una Prueba de Concepto (PoC) para la migración de datos históricos a un nuevo sistema de base de datos, integrando múltiples funcionalidades:
  
- **Migración de datos históricos:** Importación de archivos CSV (localmente o desde S3) hacia PostgreSQL.
- **Servicio REST con FastAPI:** Permite la inserción de nuevas transacciones en batch (de 1 hasta 1000 registros por solicitud) y la restauración de datos desde backups.
- **Backup y Restauración:** Genera backups en formato AVRO de cada tabla y permite restaurarlos usando inserción en batch.

## Setup
1. Create a virtual environment:
    ```sh
    python -m venv venv
    ```
2. Activate the virtual environment:
        ```
        source venv/bin/activate
        ```
3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Project Structure
- **api/**  
  - Contiene el código de la API REST, incluyendo endpoints para la migración, inserción batch y backup/restauración.
  - **models/**: Definición de modelos SQLAlchemy.
  - **routes/**: Endpoints específicos (por ejemplo, batch insertion y restore).
  - **config.py**: Configuración del entorno (DB, AWS, rutas, etc.), que carga variables de entorno de forma condicional (local vs. producción).

- **services/**  
  - Funciones de respaldo y restauración de datos en formato AVRO.
  
- **scripts/**  
  - Scripts para la migración de datos históricos desde CSV (local y desde S3).
  
- **data/migration_logs/**  
  - Directorio local para almacenar logs de limpieza de datos antes de ser subidos a S3.

- **Dockerfile y docker-compose.yml**  
  - Archivos para contenerización y despliegue, facilitando una configuración consistente en desarrollo y producción (Render).

- **Reportes**
  - Archivos pdf con los resultados obtenidos con base en las consultas solicitadas en el challenge 2. (Ver en QlikSense también).

- **Interfaz de Demo (Tkinter):**  
  - Una pequeña aplicación de escritorio que permite probar la API (migración, restore, etc.) de forma interactiva.

## Requisitos

- **Python 3.8+**
- **PostgreSQL**
- **AWS S3:** Acceso mediante claves configuradas con `boto3`.
- **Dependencias:** Las dependencias se listan en `requirements.txt` e incluyen:
  - fastavro
  - pandas
  - boto3
  - fastapi
  - uvicorn
  - sqlalchemy
  - python-dotenv
  - requests
  - tkinter (incluido en Python en la mayoría de sistemas)
  
## Posibles MejoraS

- **Migración desde S3:** Automatizar y optimizar la descarga y carga de archivos CSV desde S3 para reducir la intervención manual.
- **Guardar Logs en S3:** Implementar un sistema de monitoreo centralizado y análisis de logs para mejorar la trazabilidad y auditoría.
- **Seguridad:** Integrar AWS Secrets Manager (o una solución similar) para gestionar de forma segura las credenciales y mejorar las políticas de acceso.
- **Manejo de Constantes:** Centralizar la configuración de rutas, tamaños de batch y otros parámetros críticos utilizando herramientas como `pydantic.BaseSettings`.
- **Validaciones de JSON:** Ampliar y robustecer la validación de la estructura de los JSON en los endpoints mediante modelos Pydantic para garantizar la integridad de los datos.
- **Backup e Inserción en Batch:** Optimizar el proceso de restauración de backups para manejar grandes volúmenes de datos de forma eficiente.
