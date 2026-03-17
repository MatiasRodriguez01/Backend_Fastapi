# Dependencias necesarias:
# - motor.motor_asyncio (cliente MongoDB asíncrono)
# - FastAPI Depends (para inyección en endpoints)

from ...infraestructura.db.mongo_connection import MongoConnection
from ...infraestructura.repositories.user_repositories_mongo import UserRepositoryMongo

from ...infraestructura.security.Settings import Settings 

# GetCollection.py
# Dependencia para obtener una colección de MongoDB.
# Se utiliza en los repositorios para acceder a la base de datos.
# Retorna una instancia de la colección solicitada.

def get_users_collection():
    connection = MongoConnection(uri="mongodb://localhost:27017", db_name="local")
    return UserRepositoryMongo(connection)


def get_collection():
    URL = Settings().MONGODB_URL
    DATABASE = Settings().DATABASE
    connection = MongoConnection(uri=URL, db_name=DATABASE)
    return UserRepositoryMongo(connection)