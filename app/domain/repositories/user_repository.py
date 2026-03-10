# Dependencias necesarias: 
# - Dependencia estándar de Python para clases abstractas
# - Entidad de dominio que representa al usuario
# - Tipado opcional para mayor claridad
from abc import ABC, abstractmethod   
from ...domain.entities.user import User 
from typing import Optional           

# user_repository.py
# Repositorio abstracto de usuarios.
# - Define la interfaz que deben implementar los repositorios concretos
#   (ejemplo: UserRepositoryMongo).
# - Contiene operaciones básicas de persistencia y consulta de usuarios.

class UserRepository(ABC): 
    """
    Interfaz abstracta para repositorios de usuarios.
    Define los métodos que cualquier implementación debe proveer.
    """

    @abstractmethod
    def users(self) -> list[Optional[User]]:
        """
        Devuelve la lista de todos los usuarios registrados.
        """
        pass

    @abstractmethod
    def get_by_query(self, key: str, value: str) -> Optional[User]:
        """
        Busca un usuario filtrando por un campo específico.
        Ejemplo: key="email", value="test@mail.com".
        """
        pass

    @abstractmethod
    def create(self, user: User) -> Optional[User]:
        """
        Crea un nuevo usuario en el repositorio.
        Retorna el usuario creado o None si falla.
        """
        pass

    @abstractmethod
    def update(self, user: User) -> Optional[User]:
        """
        Actualiza un usuario existente.
        Retorna el usuario actualizado o None si falla.
        """
        pass

    @abstractmethod
    async def update_password(self, id: str, password: str) -> Optional[User]:
        """
        Actualiza el password de un usuario existente.
        Retorna el usuario actualizado o None si falla.
        """
        pass

    @abstractmethod
    def delete_user(self, id: str) -> bool:
        """
        Elimina un usuario por su ID.
        Retorna True si la operación fue exitosa, False en caso contrario.
        """
        pass