from fastapi import FastAPI
from api.routes import jobs, departments, hired_employees, backup, migrate
from api.routes.migrate import migrate_data

app = FastAPI(title="Data Migration Globant API", version="0.1.0")

# Incluir las rutas de cada entidad
app.include_router(jobs.router)
app.include_router(departments.router)
app.include_router(hired_employees.router)
app.include_router(backup.router)
app.include_router(migrate.router) # por terminar.

@app.get("/")
def home():
    return {"mensaje": "Bienvenidos a la API de Data Migration Globant"}