from Domain.entities.user import User
from Domain.repositories.user_repository import UserRepository
from aplicacion.security.pass_hasher import hash_password

class CreateUserUseCase:

    def __init__(self, repository: UserRepository):
        self.repository = repository


    def register(self, username: str, password: str, email: str, age: int) -> User:
        hashed = hash_password(password)

        user = User(
            username=username,
            password=hashed,
            email=email,
            age=age
        )

        return self.repository.create(user)

    def users(self) -> list[User]:
        return self.repository.users()

    def show_user(self, username: str) -> User | None:
        return self.repository.get_by_username(username)
