from Domain.entities.user import User
from Domain.repositories.user_repository import UserRepository

from aplicacion.security.pass_hasher import verify_password

class LoginUserUseCase:

    def __init__(self, repository: UserRepository):
        self.repository = repository

    def login(self, username: str, password: str) -> User | None:    
        user = self.repository.get_by_username(username)
        
        if not verify_password(password, user.password):
            raise ValueError("Contraseña incorrecta")
        
        return user
        
        