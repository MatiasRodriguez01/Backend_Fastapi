from application.security.pass_hasher import hash_password
from typing import Optional

from domain.repositories.user_repository import UserRepository
from domain.entities.user import User
from domain.value_objects.role import RoleUser

class RegisterUserUseCase:

    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def execute(self, username: str, password: str, email: str, age: str) -> Optional[User]:
        role = RoleUser.CLIENT.value
        hashed = hash_password(password)

        user = User(
            username=username,
            password=hashed,
            email=email,
            role=role,
            age=age
        )

        return self.repository.create(user)