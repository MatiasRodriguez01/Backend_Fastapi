# Dependencias necesarias:
# - fastapi (para levantar el servidor)
# - api.routers (para importar las rutas)
from fastapi import FastAPI
from api.routers import users

# main.py
# Levantemos la API en este archivo, y incluimos sus rutas
app = FastAPI() 

app.include_router(users.router)
