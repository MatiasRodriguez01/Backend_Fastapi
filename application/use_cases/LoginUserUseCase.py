from domain.repositories.user_repository import UserRepository
from application.security.pass_hasher import verify_password
from typing import Optional
from domain.entities.user import User

class LoginUserUseCase:
    def __init__(self, repository: UserRepository):
        self.repository = repository


    async def execute(self, username: str, password: str) -> Optional[User]:

        payload = self.repository.get_by(key="username", value=username)

        if not verify_password(password, payload.password):
            raise ValueError("Contraseña Incorrecta")
        
        return payload