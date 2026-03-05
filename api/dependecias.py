from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timezone
from aplicacion.security.settings import Settings

from api.schemas.user_schemas import UserCreate
from infraestructura.db.mongo_connection import collection

# Con esto extraemos el token JWT desde el header Authorization
OAUTH2_LOGIN = OAuth2PasswordBearer(
    tokenUrl="login",
    auto_error=False
)

# AQUI VAMOS A EVALUAR SI EL USUARIO INGRESADO SE PUEDE REGISTRAR
async def validate_user_fields(user: UserCreate):
    # Con el 'metodo model_dump()' abstraemos los items del usuario
    data = user.model_dump()
    
    # Con este for, verificamos si todos los campos esta requeridos
    # menos el id, porque lo genera la misma collecion de la BD
    for key, value in data.items():
        if key != "id" and value is "":
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail=f"El campo '{key}' es obligatorio",
                headers={"WWW-Authenticate": "Bearer"}
            )
        # Evaluamos si el formato de email, es correcto
        if (key == "email") and ("@" not in value or "." not in value):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail=f"El Email ingresado es Invalido",
                headers={"WWW-Authenticate": "Bearer"}
            )
        # Y verificamos si la edad no es negativa
        if key == "age" and value <= 0:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail=f"La Edad No Debe Ser Negativa",
                headers={"WWW-Authenticate": "Bearer"}
            )
    # Verificamos si los campos que recibe la ruta esta repetidos
    for key, value in data.items():
        # Menos la edad, id y el role esos no se evaluan
        if key != "id" and key != "age" and collection.find_one({key: value}):        
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail=f"El usuario Existe, el '{key}': '{value}' se esta usando",
                headers={"WWW-Authenticate": "Bearer"}
            )
    # Si todo esta bien la dependencia retorna el usuario ingresado
    return user


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
    