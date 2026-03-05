from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timezone
from infraestructura.security.settings import Settings

# Con esto extraemos el token JWT desde el header Authorization
OAUTH2_LOGIN = OAuth2PasswordBearer(
    tokenUrl="login",
    auto_error=False
)

# AQUI EVALUAMOS SI EL TOKEN INGRESADO ES VALIDO
async def required_auth(token: str = Depends(OAUTH2_LOGIN)):
    # Vemos si el usuario ingreso el token de acceso
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Ingrese un Token de Autenticación",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try: 
        # Decodificamos el token para verificar sus atributos
        payload = jwt.decode(token, Settings.SECRET_KEY, algorithms=[Settings.ALGORITHM])
        # Con variable 'now' obtenemos la hora actual
        now = int(datetime.now(timezone.utc).timestamp())
        # Y con esta condicion evaluamos si el token expiro
        # Con esta condicion, si el tiempo de expiracion es menor al tiempo de ahora
        if payload.get("exp") < now:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="El token ha expirado",
                headers={"WWW-Authenticate": "Bearer"},
            )
    # Evaluamos si las credenciales son incorrectas
    except JWTError:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales De Autenticación Inválidas",
                headers={"WWW-Authenticate": "Bearer"}
            )
    