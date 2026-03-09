# Dependencias necesarias:
# - Entidad de dominio que representa al usuario
# - Interfaz abstracta de repositorio de usuarios
# - Función para obtener la colección MongoDB
# - Tipado opcional y listas para mayor claridad
# - ObjectId de bson para trabajar con identificadores de MongoDB
# - CryptContext de passlib para encriptar y verificar contraseñas

from domain.entities.user import User
from domain.repositories.user_repository import UserRepository

from infraestructura.db.mongo_connection import MongoConnection

from bson.objectid import ObjectId 
from bson.errors import InvalidId

from typing import Optional
from passlib.context import CryptContext



crypt = CryptContext(schemes=["bcrypt"])

# user_repositories_mongo.py
# Implementación concreta del repositorio de usuarios utilizando MongoDB.
# Extiende la interfaz UserRepository definida en Domain/repositories/user_repository.py.
# Contiene las operaciones CRUD (crear, leer, eliminar) sobre la colección de usuarios.

def user(payload: any) -> User:
    return User(
                id=str(payload["_id"]),
                username=payload["username"],
                password=payload["password"],
                email=payload["email"],
                role=payload["role"],
                age=payload["age"]
            )

class UserRepositoryMongo(UserRepository):
    """
    Implementación del repositorio de usuarios en MongoDB.
    """

    def __init__(self, connection: MongoConnection):
        super().__init__(),
        self.collection = connection.get_collection("users")
        
    async def users(self) -> list[User]:
        """
        Devuelve la lista de todos los usuarios registrados.
        """
        cursor = self.collection.find({})
        return [ user(data) async for data in cursor]
    
    async def get_by_id(self, id: str) -> Optional[User]:
        """
        Obtiene un usuario por su identificador único.
        """
        try:
            oid = ObjectId(id)
            payload = await self.collection.find_one({"_id": oid})

            if payload:
                return user(payload)
            return None
        except InvalidId:
            return None

    async def get_by_query(self, key: str, value: str) -> Optional[User]:
        """
        Busca un usuario filtrando por un campo específico.
        Ejemplo: key="email", value="test@mail.com".
        """
        if key == "id":
            value = ObjectId(value)
            payload = await self.collection.find_one({"_id": value})
        else:
            payload = await self.collection.find_one({key: value})

        if payload:
            return user(payload)
        return None


    async def create(self, user: User) -> Optional[User]:
        """
        Crea un nuevo usuario en el repositorio.
        Retorna el usuario creado o None si falla.
        """

        result = await self.collection.insert_one({
            "username": user.username,
            "password": user.password,
            "email": user.email,
            "role": user.role,
            "age": user.age
        })

        user.id = str(result.inserted_id)
        return user

    async def delete_user(self, id: str) -> bool:
        """
        Elimina un usuario por su ID.
        Retorna True si la operación fue exitosa, False en caso contrario.
        """
        try:
            oid = ObjectId(id)        
            result = await self.collection.find_one_and_delete(
                {"_id": oid}
            )
        
            if result: 
                return result
            return None
        except InvalidId:
            return None
    
        

