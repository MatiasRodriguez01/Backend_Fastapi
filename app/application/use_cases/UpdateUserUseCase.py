from ...domain.entities.user import User
from ...domain.repositories.user_repository import UserRepository

from ...api.schemas.user_schemas import UserUpdate

from ...infraestructura.security.HashPassword import hash_password

from typing import Optional

class UpdateUserUseCase:
    def __init__(self, repository: UserRepository):
        self.repository = repository


    async def execute(self, id: str, 
                            user: UserUpdate) -> Optional[User]:
        
        hashed_password = None
        if user.password is not None:
            hashed_password = hash_password(user.password)
            user.password = hashed_password

        payload: User = await self.repository.update(id, user)
        return payload if payload else None