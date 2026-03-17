from fastapi import APIRouter, status, HTTPException, Depends, dependencies

from ...domain.entities.user import User
from ...api.schemas.user_schemas import UserResponse, user_response, UserCreate

from ...infraestructura.repositories.user_repositories_mongo import UserRepositoryMongo
from ...application.use_cases.UpdateUserUseCase import UpdateUserUseCase
from ...application.use_cases.GetUserByQueryUseCase import GetUserByQueryUseCase

from ..dependencias.GetCollection import get_collection
from ..dependencias.UserValidate import  validate_user_fields 
from ..dependencias.TokenValidate import  required_auth

from ...domain.value_objects.role import RoleUser

router = APIRouter(
    prefix="/update",
    tags=["update"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Ruta no encontrada"}}
)


@router.put("/{id}", dependencies=[Depends(required_auth)])
async def update_user(id: str, 
                      user: UserCreate,
                      repo: UserRepositoryMongo = Depends(get_collection)) -> UserResponse:

    use_case = UpdateUserUseCase(repo)
    new_user: User = await use_case.execute(id, user)
    if new_user is None:
        return {
            "detail": "No se pudo actualizar"
        }
    return user_response(user)
