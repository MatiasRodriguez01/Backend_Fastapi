# Dependencias necesarias:
# - UserRepositoryMongo (operación de borrado en MongoDB)

from ...domain.repositories.user_repository import UserRepository

# DeleteUserUseCase.py
# Caso de uso: eliminar un usuario por su ID.
# - Verifica existencia del usuario.
# - Elimina el registro de la base de datos.
# - Devuelve confirmación o error si no existe.

class DeleteUserUseCase: 
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def execute(self, id: str) -> bool:
        value: bool = await self.repository.delete_user(id)
        return value 