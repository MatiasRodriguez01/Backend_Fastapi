import pytest
from app.infraestructura.db.mongo_connection import MongoConnection
from app.infraestructura.security.Settings import Settings
from motor.motor_asyncio import AsyncIOMotorCollection

URL = Settings().MONGODB_URL
DB_NAME = Settings().DATABASE

@pytest.mark.asyncio
async def test_get_collection_name():
    mongo_connection = MongoConnection(URL, DB_NAME)
    collection: AsyncIOMotorCollection = mongo_connection.get_collection("users")
    assert collection.name == "users"