from pydantic import BaseModel # Usamos BaseModel para facilitar la creacion de las clases
from domain.entities.user import User # importamos el dominio
from domain.value_objects.role import RoleUser # importamos el role

# Usamos 2 proyecciones, para facilitar las transferencia de datos y no exponer el dominio
# 'UserCreate' lo usamos para crear un usuario nuevo con los datos necesarios
class UserCreate(BaseModel):
    id: str | None = None
    username: str
    password: str
    email: str
    age: int
# 'UserResponse' es el schema que devuelven los getters de las rutas, para no exponer las contraseñas de los usuarios
class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    role: str
    age: int
# Esta funcion recibe el dominio y devuelve la proyeccion 'UserResponse', con los datos del mismo
def user_response(user: User) -> UserResponse:

    role = user.role
    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        role=role,
        age=user.age
    )
# Esta funcion recibe una lista del dominio y devuelve una lista de 'UserResponse'
def users_response(users: list[User]) -> list[UserResponse]:
    return [user_response(user) for user in users]