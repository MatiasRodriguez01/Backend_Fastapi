# Dependencias necesarias:
# - UserRepositoryMongo (consulta por ID en MongoDB)
# - Entidad de dominio que representa al usuario
# - Tipado opcional para mayor claridad

from domain.repositories.user_repository import UserRepository
from typing import Optional
from domain.entities.user import User

# GetUserByIdUseCase.py
# Caso de uso: obtener un usuario por su ID único.
# - Busca en la base de datos usando el identificador.
# - Devuelve el objeto usuario si existe.

class GetUserByIdUseCase: 
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def execute(self, id: str) -> Optional[User]:
        user = await self.repository.get_by_id(id)
        
        if user:
            return user
        return None