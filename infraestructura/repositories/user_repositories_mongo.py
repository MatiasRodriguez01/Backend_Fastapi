from Domain.entities.user import User
from Domain.repositories.user_repository import UserRepository

from infraestructura.db.client import collection

from passlib.context import CryptContext

crypt = CryptContext(schemes=["bcrypt"])

class UserRepositoryMongo(UserRepository):

    def get_by_username(self, username: str) -> User | None:
        
        payload = collection.find_one({"username": username}) 
        if not payload: 
            raise { "error": "Usuario No Encontrado" }
            
        return User(
            id=str(payload["_id"]),
            username=payload["username"],
            password=payload["password"],
            email=payload["email"],
            age=payload["age"]
        )
        
    
    def create(self, user: User) -> User:
        result = collection.insert_one({
            "username": user.username,
            "password": user.password,
            "email": user.email,
            "age": user.age
        })

        user.id = str(result.inserted_id)
        return user

    def users(self) -> list[User]:
        return [ User(
                        id=str(data["_id"]),
                        username=data["username"],
                        password=data["password"],
                        email=data["email"],
                        age=data["age"]
                ) for data in collection.find() ]

