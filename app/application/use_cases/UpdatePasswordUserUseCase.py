from ...domain.entities.user import User
from ...domain.repositories.user_repository import UserRepository

from ...api.schemas.user_schemas import UserUpdate

from ...infraestructura.security.HashPassword import hash_password

from typing import Optional

class UpdatePasswordUserUseCase:
    def __init__(self, repository: UserRepository):
        self.repository = repository


    async def execute(self, id: str, 
                            password: str) -> Optional[User]:

        if password is None:
            return None        
        
        hashed_password = hash_password(password)
        payload: User = await self.repository.update_password(id, hashed_password)
        return payload if payload else None