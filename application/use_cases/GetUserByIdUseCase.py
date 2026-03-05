from domain.repositories.user_repository import UserRepository
from typing import Optional
from domain.entities.user import User

class GetUserByIdUseCase: 
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def execute(self, id: str) -> Optional[User]:
        user = await self.repository.get_by_id(id)
        return user if user else None