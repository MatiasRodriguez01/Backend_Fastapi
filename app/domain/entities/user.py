# Importamos RoleUser para asignar Roles a los usuarios
from ...domain.value_objects.role import RoleUser

# Dominio
class User:
    def __init__(self, 
                 username: str, 
                 password: str, 
                 email: str, 
                 age: int,
                 role: RoleUser,
                 id: str | None = None):
        self.id = id
        self.username = username
        self.password = password
        self.email = email
        self.age = age
        self.role = role