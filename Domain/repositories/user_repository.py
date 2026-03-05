from abc import ABC, abstractmethod
from domain.entities.user import User
from typing import Optional 

class UserRepository(ABC):

    @abstractmethod
    def create(self, user: User) -> Optional[User]:
        pass
    
    @abstractmethod
    def users(self) -> list[Optional[User]]:
        pass
    
    @abstractmethod
    def get_by_query(self, key: str, value: str) -> Optional[User]:
        pass

    @abstractmethod
    def get_by_id(self, id: str) -> Optional[User]:
        pass

    @abstractmethod
    def delete_user(self, id: str) -> bool:
        pass
