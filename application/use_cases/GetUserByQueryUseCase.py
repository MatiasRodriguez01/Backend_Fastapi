from domain.repositories.user_repository import UserRepository
from typing import Optional
from domain.entities.user import User

class GetUserByQueryUseCase: 
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def execute(self, key: str, value: str) -> Optional[User]:

        user = await self.repository.get_by_query(key= key, value=value)
        
        if user:
            return True
        return False
    
    