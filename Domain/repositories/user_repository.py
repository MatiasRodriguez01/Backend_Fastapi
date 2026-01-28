from abc import ABC, abstractmethod
from Domain.entities.user import User


class UserRepository(ABC):

    @abstractmethod
    def create(self, user: User) -> User:
        pass
    
    def users(self) -> list[User]:
        pass

    @abstractmethod
    def get_by_username(self, username: str) -> User | None:
        pass
    
