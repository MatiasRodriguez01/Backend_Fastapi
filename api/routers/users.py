from fastapi import APIRouter, status, HTTPException, Depends, dependencies
from fastapi.security import OAuth2PasswordRequestForm

from api.schemas.user_schemas import UserCreate, UserResponse, user_response, users_response

from application.use_cases.GetUserByIdUseCase import GetUserByIdUseCase
from application.use_cases.GetUserByQueryUseCase import GetUserByQueryUseCase
from application.use_cases.ListUsersUseCase import ListUsersUseCase
from application.use_cases.LoginUserUseCase import LoginUserUseCase
from application.use_cases.RegisterUserUseCase import RegisterUserUseCase
from application.use_cases.DeleteUserUseCase import DeleteUserUseCase

from infraestructura.repositories.user_repositories_mongo import UserRepositoryMongo
from infraestructura.security.jwt_handler import create_access_token

from api.dependencias.GetCollection import  get_user_repository
from api.dependencias.UserValidate import  validate_user_fields
from api.dependencias.TokenValidate import  required_auth

# con esto logramos configurar el ROUTER
# Le damos una ruta escrita por defecto que es 'localhost:8000/users'
# Las tags donde se ve en la documentacion
# Y un error por defecto si la ruta no funciona
router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "No Funciona la Ruta usersTest"}},)

# Asignamos una excepcion para no repetirla
EXCEPTION_USER = HTTPException(status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

# Con esta ruta, hacemos el login para optener un token de acceso
# Recibe un formulario con el 'username' y el 'password'
@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends(), 
                repo: UserRepositoryMongo = Depends(get_user_repository)): # Usamos el repositorio de users como dependencia
    use_case = LoginUserUseCase(repo) # Los usos de casos que podriamos usar
    # Optenemos el usuario completo con la funcion de login
    user = await use_case.execute(form.username, form.password)
    # Y creamos el token de acceso con esta funcion usando el 'username'
    return create_access_token(user.username)

# Con esta ruta, hacemos el register para crear un usuario nuevo
# Recibe el payload, donde estas los campos necesarios para crear un usuario
@router.post("/register")
async def register(payload: UserCreate = Depends(validate_user_fields), 
                   repo: UserRepositoryMongo = Depends(get_user_repository)): # Usamos el repositorio de users como dependencia
    use_case = RegisterUserUseCase(repo) # Los usos de casos que podriamos usar
    # Creamos el usuario y lo optenemos 
    user = await use_case.execute(
        username=payload.username,
        password=payload.password,
        email=payload.email,
        age=payload.age
    )
    # Y creamos el token de acceso con esta funcion usando el 'username'
    return create_access_token(user.username)

# Con esta ruta optenemos Todos los usuarios, y asignamos una dependencia para que el usuario
# Ingrese un token de acceso
@router.get("", dependencies = [Depends(required_auth)])
async def get_users(repo: UserRepositoryMongo = Depends(get_user_repository)) -> list[UserResponse]: # Usamos el repositorio de users como dependencia) -> list[UserResponse]: # -------> retornamos una lista de usuarios
    use_case = ListUsersUseCase(repo) # Los usos de casos que podriamos usar
    # Con esta funcion, retornamos una lista con el schema 'UserResponse' para no retorna los dominios
    return users_response(await use_case.execute())

# Con esta funcion 'query' retornamos un usuario por 'key', y su valor correspondiente
@router.get("/query", dependencies = [Depends(required_auth)])
async def get_query(key: str, 
                    value: str, 
                    repo: UserRepositoryMongo = Depends(get_user_repository)) -> UserResponse: # Usamos el repositorio de users como dependencia) -> UserResponse: # -------> retornamos un usuario
    try: 
        repo = UserRepositoryMongo() # Usamos el repositorio de users
        use_case = GetUserByQueryUseCase(repo) # Los usos de casos que podriamos usar
        # Con esta funcion, retornamos el schema 'UserResponse' para no retorna el dominio
        return user_response(await use_case.execute(key, value))
    # Si no optenemos el usuario retornamos una excepcion
    except:
        raise EXCEPTION_USER


@router.get("/{id}", dependencies = [Depends(required_auth)])
async def get_by_id(id: str,
                    repo: UserRepositoryMongo = Depends(get_user_repository)) -> UserResponse:
    try: 
        repo = UserRepositoryMongo() # Usamos el repositorio de users
        use_case = GetUserByIdUseCase(repo) # Los usos de casos que podriamos usar

        return user_response(await use_case.execute(id))
    except: 
        raise EXCEPTION_USER


# Con Esta ruta Eliminamos un usuario de la BD
@router.delete("/{id}",  dependencies = [Depends(required_auth)])
async def delete_user(id: str,
                      repo: UserRepositoryMongo = Depends(get_user_repository)) -> None: # -------> No retornamos nada porque es un DELETE
    repo = UserRepositoryMongo() # Usamos el repositorio de users
    use_case = DeleteUserUseCase(repo) # Los usos de casos que podriamos usar
    # Con la funcion delete_user retornamos un booleano si lo elimino mostrara un mensaje,
    if await use_case.execute(id):
        return {"detail": "Usuario eliminado correctamente"}
    # Sino retornamos un error
    else:
        raise EXCEPTION_USER
