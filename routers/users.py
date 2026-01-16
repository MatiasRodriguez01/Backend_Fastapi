
from dataclasses import field
from db.modules.user import User
from fastapi import APIRouter, HTTPException, status
from bson import ObjectId

from db.client import db_client
from db.schemas.schemas import show_schemas, show_schema, show_fields

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


@router.get("")
async def clients():
    users = show_schemas(db_client.users.find())
    print(db_client.users.find())
    if not users:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="No hay usuarios registrados")
    return show_schemas(db_client.users.find())

@router.get("/{id}")
async def getById(id: str):

    clase = db_client.users.find_one({"_id": ObjectId(id)})
    if not clase:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return show_schema(clase)

@router.post("")
async def create(client: User):
    user_dict = dict(client)
    del user_dict["id"]

    id = db_client.users.insert_one(user_dict).inserted_id
    new_client = show_schema(db_client.users.find_one({ "_id": id }))
    
    return User(**new_client)


@router.delete("/{id}")
async def delete(id: str):

    try:
        db_client.users.delete_one({"_id": ObjectId(id)})
        return {"message": "Usuario eliminado correctamente"}
    except HTTPException as e:
        return {"error": "No se ha encontrado el usuario"}