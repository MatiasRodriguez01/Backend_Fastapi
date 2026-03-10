# Dependencias necesarias:
# - UserRepositoryMongo (consulta dinámica en MongoDB)
# - Entidad de dominio que representa al usuario
# - Tipado opcional para mayor claridad

from ...domain.repositories.user_repository import UserRepository
from typing import Optional
from ...domain.entities.user import User

# GetUserByQueryUseCase.py
# Caso de uso: obtener un usuario filtrando por un campo específico.
# - Recibe key (campo) y value (valor).
# - Devuelve el usuario que cumpla la condición.

class GetUserByQueryUseCase: 
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def execute(self, key: str, value: str) -> Optional[User]:
        user = await self.repository.get_by_query(key= key, value=value)
        
        if user:
            return user
        return None
    
    