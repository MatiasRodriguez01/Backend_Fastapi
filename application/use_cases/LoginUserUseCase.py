from domain.repositories.user_repository import UserRepository
from infraestructura.security.pass_hasher import verify_password, CryptContext, hash_password   
from typing import Optional
from domain.entities.user import User

class LoginUserUseCase:
    def __init__(self, repository: UserRepository):
        self.repository = repository


    async def execute(self, username: str, password: str) -> Optional[User]:

        payload: User = await self.repository.get_by_query(key="username", value=username)

        if payload:
            valided = verify_password(password, payload.password)
            print(valided)
            if not valided:
                raise ValueError("Contraseña Incorrecta")
            
            return payload

        return None
        
        