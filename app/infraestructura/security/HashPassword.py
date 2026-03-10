# Dependencias necesarias:
# - passlib.context.CryptContext (para encriptar y verificar contraseñas)

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# HashPassword.py
# - Descripcion: Módulo para encriptar una contraseña.
# - Salida: string hasheado
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# - Descripcion: Modulo para verificar que la contraseña es la correcta
# - Salida: booleano (si el String es igual al Hash)
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)