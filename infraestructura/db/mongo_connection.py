# Dependencias necesarias:
# - motor.motor_asyncio.AsyncIOMotorClient: cliente asíncrono para MongoDB.

from pymongo.asynchronous.mongo_client import AsyncMongoClient

# mongo_connection.py
# Archivo encargado de establecer la conexión con MongoDB.
# - Inicializa el cliente de base de datos.
# - Permite obtener la instancia de la base y sus colecciones.
# - Se utiliza en los repositorios para interactuar con MongoDB.

class MongoConnection:
    def __init__(self, uri: str, db_name: str):
        self.client = AsyncMongoClient(uri)
        self.db = self.client[db_name]

    def get_collection(self, name: str):
        """Devuelve una colección específica de la base de datos."""
        return self.db[name]

    async def close(self):
        """Cierra la conexión con MongoDB."""
        self.client.close()
