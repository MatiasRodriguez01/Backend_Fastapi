# api/dependencias.py
from infraestructura.repositories.user_repositories_mongo import UserRepositoryMongo
from infraestructura.db.mongo_connection import MongoConnection

def get_user_repository():
    connection = MongoConnection(uri="mongodb://localhost:27017", db_name="users_test")
    return UserRepositoryMongo(connection)