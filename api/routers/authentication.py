from fastapi import APIRouter, Depends, HTTPException, status  
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from jose import JWTError, jwt
from passlib.context import CryptContext

from datetime import datetime, timedelta

SECRET_KEY = "super-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1 # minutes

crypt = CryptContext(schemes=["bcrypt"])

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)

oauth2 = OAuth2PasswordBearer(
    tokenUrl="login",
    auto_error=False
)

class Item(BaseModel):
    full_name: str
    username: str
    email: str
    disabled: bool = False

class ItemInDB(Item):
    password: str

items_db = {   
    "johndoe": {
        "full_name": "John Doe",
        "username": "johndoe",
        "email": "john.doe@example.com",
        "disabled": False,
        "password": "$2a$12$BYGrAC.TuIQplzD.YaHs6.uW8ZyLDMrMAiSf1YvnKUdvvXKM4wVfy" # password: secret
    },
    "alice": {
        "full_name": "Alice Wonderland",
        "username": "alice",
        "email": "alice.wonderland@example.com",
        "disabled": True,
        "password": "$2a$12$kxDo3kj5pmAIhQs48jIDf.AEoE01Uy9DtAE/bBAE7l0T3nma8r77S" # password: wonderland
    },
}

def search_item(username: str):
    if username in items_db:
        return ItemInDB(**items_db[username])

def search(username: str):
    if username in items_db:
        return Item(**items_db[username])

async def auth_item(token: str = Depends(oauth2)):
    exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales De Autenticación Inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    expire = payload.get("exp")
    username = payload.get("sub")

    if expire < datetime.utcnow().timestamp():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="El token ha expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if token is None:
        raise HTTPException( 
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="NO tiene acceso a este recurso",
            headers={"WWW-Authenticate": "Bearer"},
        ) 
    try:
        
        if username is None:
            raise exception

    except JWTError:
        raise exception

    return username

async def current_item(item: Item = Depends(auth_item)):
    if not item:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Usuario no autenticado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not item.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Usuario inactivo"
        )
    
    return item

@router.get("/me")
async def me(item: Item = Depends(current_item)):
    return item

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):

    item_db = items_db.get(form.username)
    if not item_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")
    
    item = search_item(form.username)

    if not crypt.verify(form.password, item.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")
    
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)

    access_token = {
        "sub": item.username,
        "exp": expire
    }

    token = jwt.encode(access_token, SECRET_KEY, algorithm=ALGORITHM)
    
    return {
        "access_token": token,
        "token_type": "bearer"
    }

