from domain.repositories.user_repository import UserRepository
from typing import Optional
from domain.entities.user import User

class ListUsersUseCase: 
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def execute(self) -> list[Optional[User]]:
        return self.repository.users()