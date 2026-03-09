# Dependencias necesarias:
# - UserRepositoryMongo (persistencia en MongoDB)
# - infraestructura.security.pass_hasher (hash de contraseñas) 
# - Entidad de dominio que representa al usuario
# - Tipado opcional para mayor claridad
# - domain.value_objects.role (definición de roles) 

from infraestructura.security.pass_hasher import hash_password
from typing import Optional 

from domain.repositories.user_repository import UserRepository
from domain.entities.user import User
from domain.value_objects.role import RoleUser

# RegisterUserUseCase.py
# Caso de uso: registrar un nuevo usuario en la base de datos.
# - Crear un role predeterminado (CLIENT)
# - Encripta la contraseña antes de guardar.
# - Devuelve el usuario creado.

class RegisterUserUseCase:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def execute(self, username: str, password: str, email: str, age: str) -> Optional[User]:
        role = RoleUser.CLIENT.value
        hashed = hash_password(password)

        user = User(
            username=username,
            password=hashed,
            email=email,
            role=role,
            age=age
        )

        user_registered = await self.repository.create(user)
        return user_registered if user_registered else None