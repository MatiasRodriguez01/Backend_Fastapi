# Dependencias necesarias:
# - enum (definición de enumeraciones para roles de usuario)
from enum import Enum

# role.py
# - Creamos un rol de usuario
class RoleUser(Enum):
    ADMIN = "admin",
    CLIENT = "client"