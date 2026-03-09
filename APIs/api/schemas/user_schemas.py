# Dependencias necesarias:
# - pydantic BaseModel (para facilitar creacion de modelos)
# - domain.entities.user (para validar modelos)
# - domain.value_objects.role (para asignar valores)

from pydantic import BaseModel 
from domain.entities.user import User 
from domain.value_objects.role import RoleUser 

# SCHEMAS
# - Modelo para crear usuarios nuevos
class UserCreate(BaseModel):
    id: str | None = None
    username: str
    password: str
    email: str
    age: int
# - Modelo para retornar informacion
class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    role: str
    age: int

# FUNCIONES
# - Descripcion: retornar un modelo tipo 'UserReponse'
# - Entrada: usuario (dominio) tipo 'User'
# - Salida: Objeto tipo 'UserResponse'
def user_response(user: User) -> UserResponse:

    role = user.role
    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        role=role,
        age=user.age
    )
    
# - Descripcion: retornar una lista de tipo 'UserReponse'
# - Entrada: Lista de usuarios de tipo 'User'
# - Salida: Lista de tipo 'UserResponse'
def users_response(users: list[User]) -> list[UserResponse]:
    return [user_response(user) for user in users]