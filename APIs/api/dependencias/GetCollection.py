# Dependencias necesarias:
# - motor.motor_asyncio (cliente MongoDB asíncrono)
# - FastAPI Depends (para inyección en endpoints)

from infraestructura.repositories.user_repositories_mongo import UserRepositoryMongo
from infraestructura.db.mongo_connection import MongoConnection

# GetCollection.py
# Dependencia para obtener una colección de MongoDB.
# Se utiliza en los repositorios para acceder a la base de datos.
# Retorna una instancia de la colección solicitada.

def get_user_repository():
    connection = MongoConnection(uri="mongodb://localhost:27017", db_name="local")
    return UserRepositoryMongo(connection)