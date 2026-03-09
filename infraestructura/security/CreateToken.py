# Dependencias necesarias:
# - jose.jwt (para codificar y decodificar JWT)
# - datetime (para manejar expiración de tokens)
# - settings/config (clave secreta y algoritmo de firma)

from datetime import datetime, timedelta, timezone
from jose import jwt
from infraestructura.security.Settings import Settings

# CreateToken.py
# Módulo de seguridad encargado de generar tokens JWT.
# - Recibe el username del usuario autenticado.
# - Crea un token firmado con clave secreta y tiempo de expiración.
# - Devuelve el token para ser usado en futuras solicitudes protegidas.

def create_access_token(username: str):
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=Settings.ACCESS_TOKEN_DURATION)
    
    access_token = {
        "sub": username,
        "exp": expire
    }
    token = jwt.encode(access_token, Settings.SECRET_KEY, algorithm=Settings.ALGORITHM)
    
    return {
        "access_token": token,
        "token_type": "bearer"
    }