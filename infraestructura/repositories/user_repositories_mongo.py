from domain.entities.user import User
from domain.repositories.user_repository import UserRepository

from passlib.context import CryptContext
from typing import Optional

from bson.objectid import ObjectId 
from bson.errors import InvalidId

from infraestructura.db.mongo_connection import MongoConnection

crypt = CryptContext(schemes=["bcrypt"])

def user(payload: any) -> Optional[User]:
    return User(
                id=str(payload["_id"]),
                username=payload["username"],
                password=payload["password"],
                email=payload["email"],
                role=payload["role"],
                age=payload["age"]
            )

class UserRepositoryMongo(UserRepository):

    # Hacemos una superclase de UserRepository
    # Que contiene una funcines de UserRepository, y una collection (local de la clase) para la base de datos
    def __init__(self, connection: MongoConnection):
        super().__init__(),
        self.collection = connection.get_collection("users_test")
        
    # Aca devolvemos el usuario por id
    def get_by_id(self, id) -> Optional[User]:
        
        try:
            # Usamos el ObjectId para encontrarlo en la base de datos
            oid = ObjectId(id)
            payload = self.collection.find_one({"_id": oid})

            if not payload: 
                return None
            
            return user(payload)
        except InvalidId:
            return None

    # Aca devolvemos el usuario por query, selecionando la clave y su valor
    def get_by_query(self, key: str, value: str) -> Optional[User]:
        # Si la clave es por 'id' usamos el objectId
        if key == "id":
            value = ObjectId(value)
            payload = self.collection.find_one({"_id", value})
        else:
            payload = self.collection.find_one({key: value})

        if payload is None:
            return None
        
        return user(payload)

    # Retornamos una lista de usuarios
    def users(self) -> list[User]:
        return [ user(data) for data in self.collection.find() ]

    # Aca creamos un usuario nuevo
    def create(self, user: User) -> Optional[User]:

        result = self.collection.insert_one({
            "username": user.username,
            "password": user.password,
            "email": user.email,
            "role": user.role,
            "age": user.age
        })

        user.id = str(result.inserted_id)
        return user

    # Eliminamos un usuario y devuelve un booleano
    def delete_user(self, id: str) -> bool:
        oid = ObjectId(id)
        
        result = self.collection.find_one_and_delete(
            {"_id": oid}
        )

        return result is not None
        

