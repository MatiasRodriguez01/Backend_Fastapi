# Dependencias necesarias:
# - fastapi (para levantar el servidor)
# - api.routers (para importar las rutas)
from fastapi import FastAPI
from .api.routers import users, update

# main.py
# Levantemos la API en este archivo, y incluimos sus rutas
api = FastAPI() 

api.include_router(users.router)
api.include_router(update.router)
