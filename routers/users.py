from db.modules.user import User
from fastapi import APIRouter, HTTPException, status, Depends, Body
from bson import ObjectId

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext            

from db.client import db_client
from db.schemas.schemas import show_schemas, show_schema, show_fields



bcrypt = CryptContext(schemes=["bcrypt"])

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

router = APIRouter(
    prefix="/usuarios",
    tags=["usuarios"],
    responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}}
)

def search_user(field: str, key):
    try:
        client_search = db_client.users.find_one({field: key})
        return User(**show_schema(client_search))
    except:
        return {"error": "No se ha encontrado el usuario"}

@router.post("/register")
async def register(form: User):
    user_dict = {
        "username": form.username,
        "password": bcrypt.hash(form.password),
        "email": form.email,
        "age": form.age
    }

    id = db_client.users.insert_one(user_dict).inserted_id
    return search_user("_id", ObjectId(id))

@router.get("")
async def clients():
    users = show_schemas(db_client.users.find())
    if not users:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="No hay usuarios registrados")
    return users

@router.get("/{id}")
async def getById(id: str):
    try: 
        return search_user("_id", ObjectId(id))
    except:
         raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

@router.post("")
async def create(client: User):

    if search_user("username", client.username):
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="El usuario ya existe")
    
    user_dict = dict(client)
    del user_dict["id"]

    id = db_client.users.insert_one(user_dict).inserted_id
    return search_user("_id", ObjectId(id))


@router.delete("/{id}")
async def delete(id: str):

    try:
        db_client.users.delete_one({"_id": ObjectId(id)})
        return {"message": "Usuario eliminado correctamente"}
    except HTTPException as e:
        return {"error": "No se ha encontrado el usuario"}
    


