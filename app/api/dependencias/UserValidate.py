# Dependencias necesarias:
# - api.schemas.user_schemas (para validación de modelos)
# - fastapi.HTTPException y status (para devolver errores claros)
# - infraestructura.db.mongo_connection (para acceder brevemente a la BD)

from fastapi import HTTPException, status
from ...api.schemas.user_schemas import UserCreate
from ...infraestructura.db.mongo_connection import MongoConnection

from bson.objectid import ObjectId

collection = MongoConnection(uri="mongodb://localhost:27017", db_name="local").get_collection("users")

# UserValidate.py
# Dependencia para validar campos de usuario en operaciones de registro.
# - Verifica formato de email, longitud de edad.
# - Lanza excepciones HTTP si los datos no cumplen los requisitos.
# Se utiliza en el endpoint de /register para asegurar integridad de datos.
  
async def validate_user_fields(user: UserCreate):
    data = user.model_dump() # transformamos en dict para iterar sobre sus campos
    
    keys = ["username", "password", "email", "age"] # Campos obligatorios
    # recorremos cada 'item' y su valor
    for key, value in data.items():
        if (key in keys) and (value is ""): # El id no sera requerido y el valor no puede estar vacio
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail=f"El campo '{key}' es obligatorio",
                headers={"WWW-Authenticate": "Bearer"}
            )
        if (key == "email") and ("@" not in value or "." not in value): # Evaluamos si el formato de email, es correcto
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail=f"El Email ingresado es Invalido",
                headers={"WWW-Authenticate": "Bearer"}
            )
        if key == "age" and value <= 0: # Y verificamos si la edad no es negativa
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail=f"La Edad No Debe Ser Negativa",
                headers={"WWW-Authenticate": "Bearer"}
            )

    # Verificamos valores repeditos repetidos
    keys = ["id", 'age'] # campos que no se evaluaran

    for key, value in data.items():
        payload = await collection.find_one({key: value})
        if key not in keys and payload:  # Evaluaran si algun campo esta repetido en la base de datos
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail=f"El usuario Existe, el '{key}': '{value}' se esta usando",
                headers={"WWW-Authenticate": "Bearer"}
            )

    return user

async def user_search(id: str):
    object_id = ObjectId(id) # Convertimos el string a ObjectId
    payload = await collection.find_one({"_id": object_id})
            
    if (payload is None):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con id '{id}' no encontrado",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return id
    