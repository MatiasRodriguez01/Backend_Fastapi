
from dataclasses import field
from tkinter import S
from xmlrpc.client import boolean
from modules.client import Client
from fastapi import APIRouter, HTTPException, status
from bson import ObjectId

from db.client import db_client
from schemas.client_schema import client_schema, clients_schema

router = APIRouter(
    prefix="/clientes",
    tags=["clientes"],
    responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}}
)

def search_user(field: str, key):

    try:
        client_search = db_client.find_one({field: key})
        return Client(**client_schema(client_search))
    except:
        return {"error": "No se ha encontrado el usuario"}


@router.get("")
async def clients():
    return clients_schema(db_client.find())


@router.get("/{id}")
async def getById(id: str):
    return search_user("_id", ObjectId(id))


@router.post("")
async def create(client: Client):
    user_dict = dict(client)
    del user_dict["id"]

    id = db_client.insert_one(user_dict).inserted_id
    new_client = client_schema(db_client.find_one({ "_id": id }))
    
    return Client(**new_client)


@router.delete("/{id}")
async def delete(id: str):

    client = client_schema(db_client.find_one_and_delete({ "_id": ObjectId(id)}))

    if client: 
        return { "message" : "El Cliente fue eliminado"} 
    else:
        return {"error": "No se ha eliminado el usuario"}