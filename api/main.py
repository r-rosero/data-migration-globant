from fastapi import FastAPI
from api.routes import jobs, departments, hired_employees

app = FastAPI(title="Data Migration Globant API", version="0.1.0")

# Incluir las rutas de cada entidad
app.include_router(jobs.router)
app.include_router(departments.router)
app.include_router(hired_employees.router)

@app.get("/")
def home():
    return {"message": "Bienvenidos a la API de Data Migration Globant"}