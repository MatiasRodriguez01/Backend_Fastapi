# Dependencias necesarias:
# - UserRepository (acceso a la base de datos)
# - bcrypt / passlib (para verificar contraseñas encriptadas)
# - Entidad de dominio que representa al usuario
# - Tipado opcional para mayor claridad

from domain.repositories.user_repository import UserRepository
from infraestructura.security.pass_hasher import verify_password 
from typing import Optional
from domain.entities.user import User

# LoginUserUseCase.py
# Caso de uso: autenticar un usuario con username y password.
# - Valida credenciales contra el repositorio de usuarios.
# - Devuelve el objeto usuario si es válido.

class LoginUserUseCase:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def execute(self, username: str, password: str) -> Optional[User]:
        payload: User = await self.repository.get_by_query(key="username", value=username)

        if payload: # si el objeto existe
            valided = verify_password(password, payload.password)

            if not valided: # si la contraseña no coincide
                raise ValueError("Contraseña Incorrecta")
            return payload

        return None
        
        