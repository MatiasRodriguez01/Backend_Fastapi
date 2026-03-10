# Dependencias necesarias:
# - UserRepositoryMongo (consulta a la base de datos)
# - Entidad de dominio que representa al usuario
# - Tipado opcional para mayor claridad 

from ...domain.repositories.user_repository import UserRepository
from ...domain.entities.user import User
from typing import Optional

# ListUsersUseCase.py
# Caso de uso: obtener todos los usuarios registrados.
# - Consulta al repositorio de usuarios.
# - Devuelve una lista de objetos UserResponse.

class ListUsersUseCase: 
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def execute(self) -> list[Optional[User]]:

        users = await self.repository.users()
        if users:
            return users
        return []
