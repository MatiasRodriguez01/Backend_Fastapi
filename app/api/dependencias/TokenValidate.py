# Dependencias necesarias:
# - fastapi.security.OAuth2PasswordBearer (para extraer el token)
# - jose.jwt (para decodificar y validar JWT)
# - fastapi.HTTPException y status (para manejar errores HTTP)
# - infraestructura.security.settings variables de entorno

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from jose import JWTError, jwt

from datetime import datetime, timezone

from ...infraestructura.security.Settings import Settings

# TokenValidate.py
# Dependencia de seguridad para validar tokens JWT.
# - Extrae el token del encabezado Authorization.
# - Verifica su validez y decodifica el payload.
# - Lanza una excepción HTTP si el token es inválido o está vencido.
# Se utiliza en endpoints que requieren autenticación.

OAUTH2_LOGIN = OAuth2PasswordBearer(
    tokenUrl="login",
    auto_error=False
)

async def required_auth(token: str = Depends(OAUTH2_LOGIN)):

    try: 
        if token is None: # validamos si se ingreso un token de acceso
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Ingrese un Token de Autenticación",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except JWTError: 
        # decodificamos el token, y obtenemos la hora actual
        payload = jwt.decode(token, Settings.SECRET_KEY, algorithms=[Settings.ALGORITHM])
        now = int(datetime.now(timezone.utc).timestamp())
        if payload.get("exp") < now:
            raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="El token ha expirado",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales De Autenticación Inválidas",
                headers={"WWW-Authenticate": "Bearer"}
            )
    