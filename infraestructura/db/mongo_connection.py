"""
from pymongo import MongoClient
db_client = MongoClient().local
collection = db_client.users_test
"""

from pymongo.asynchronous.mongo_client import AsyncMongoClient

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
