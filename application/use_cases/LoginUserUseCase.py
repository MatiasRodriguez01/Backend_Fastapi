from domain.repositories.user_repository import UserRepository
from infraestructura.security.pass_hasher import verify_password
from typing import Optional
from domain.entities.user import User

class LoginUserUseCase:
    def __init__(self, repository: UserRepository):
        self.repository = repository


    async def execute(self, username: str, password: str) -> Optional[User]:

        payload = await self.repository.get_by_query(key="username", value=username)

        if (payload is not None) and (not verify_password(password, payload.password)):
            raise ValueError("Contraseña Incorrecta")
       
        return payload if payload else None
        
        