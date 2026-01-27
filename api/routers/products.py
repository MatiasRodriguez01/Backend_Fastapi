from fastapi import APIRouter, status, HTTPException
from api.modules.product import Product
from bson import ObjectId

from api.schemas.schemas import show_schema, show_schemas
from infraestructura.db.client import db_client

router = APIRouter(
    prefix="/productos",
    tags=["productos"],
    responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}}
)

@router.get("")
async def products():
    products = show_schemas(db_client.products.find())
    if not products:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="No hay productos registrados")
    return show_schemas(db_client.products.find())

@router.get("/{id}")
async def getById(id: str):
    product = db_client.products.find_one({"_id": ObjectId(id)})
    if not product:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    return show_schema(product)

@router.post("")
async def create(product: Product):
    product_dict = dict(product)
    del product_dict["id"]

    id = db_client.products.insert_one(product_dict).inserted_id
    new_product = show_schema(db_client.products.find_one({ "_id": id }))
    
    return Product(**new_product)

@router.delete("/{id}")
async def delete(id: str):

    try:
        db_client.products.delete_one({"_id": ObjectId(id)})
        return {"message": "Producto eliminado correctamente"}
    except HTTPException as e:
        return {"error": "No se ha encontrado el producto"}