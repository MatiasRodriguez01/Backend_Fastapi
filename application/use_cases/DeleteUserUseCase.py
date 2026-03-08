from domain.repositories.user_repository import UserRepository
from typing import Optional
from domain.entities.user import User

class DeleteUserUseCase: 
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def execute(self, id: str) -> bool:
        value: bool = await self.repository.delete_user(id)
        return value 