# Dependencias necesarias:
# FastAPI:
# - APIRouter: agrupa rutas /users | Depends: inyección de dependencias
# - HTTPException, status: manejo de errores | OAuth2PasswordRequestForm: formulario de login
from fastapi import APIRouter, status, HTTPException, Depends, dependencies
from fastapi.security import OAuth2PasswordRequestForm

# Entidades:
# - UserCreate: modelo de entrada | UserResponse: modelo de salida
# - user_response, users_response: formateo de respuestas
from ...domain.entities.user import User
from ...api.schemas.user_schemas import UserCreate, UserUpdate, UserResponse, user_response, users_response

# Casos de uso:
from ...application.use_cases.GetUserByQueryUseCase import GetUserByQueryUseCase
from ...application.use_cases.ListUsersUseCase import ListUsersUseCase
from ...application.use_cases.LoginUserUseCase import LoginUserUseCase
from ...application.use_cases.RegisterUserUseCase import RegisterUserUseCase
from ...application.use_cases.DeleteUserUseCase import DeleteUserUseCase
from ...application.use_cases.UpdateUserUseCase import UpdateUserUseCase
from ...application.use_cases.UpdatePasswordUserUseCase import UpdatePasswordUserUseCase

# Repositorio:
# - UserRepositoryMongo: acceso a MongoDB | get_user_repository: obtiene repositorio
from ...infraestructura.repositories.user_repositories_mongo import UserRepositoryMongo
from ...api.dependencias.GetCollection import  get_collection 


# Dependencias Creadas:
# - validate_user_fields: valida datos de usuario
# - required_auth: valida autenticación
from ...api.dependencias.UserValidate import  validate_user_fields, user_search
from ...api.dependencias.TokenValidate import  required_auth       

# Seguridad:
# - create_access_token: genera JWT
from ...infraestructura.security.CreateToken import create_access_token

# Excepciones
from ..exceptions.UserException import EXCEPTION_USER, EXCEPTION_USER_UPDATE, EXCEPTION_UPDATE_PASSWORD, EXCEPTION_USER_DELETE

# Configuración del router de usuarios
# Prefijo: /users
# Tags: users (para documentación automática)
# Respuesta por defecto: 404 si la ruta no existe
router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Ruta no encontrada"}
    }
)

# Endpoint: POST /login
# Descripción: Autentica al usuario con username y password.
# Entrada: OAuth2PasswordRequestForm
# Salida: Token JWT de acceso
@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends(),
                repo: UserRepositoryMongo = Depends(get_collection)):
    try:
        use_case = LoginUserUseCase(repo)
        user: User = await use_case.execute(form.username, form.password)
        return create_access_token(user.username)
    except:
        raise EXCEPTION_USER

# Endpoint: POST /register
# Descripción: Registra un nuevo usuario en la base de datos.
# Entrada: UserCreate (username, password, email, age)
# Salida: Token JWT de acceso
@router.post("/register")
async def register(payload: UserCreate = Depends(validate_user_fields),
                   repo: UserRepositoryMongo = Depends(get_collection)):
    use_case = RegisterUserUseCase(repo)
    user: User = await use_case.execute(
        username=payload.username,
        password=payload.password,
        email=payload.email,
        age=payload.age
    )
    return create_access_token(user.username)

# Endpoint: GET /users
# Descripción: Obtiene todos los usuarios registrados.
# Requiere autenticación (token JWT).
# Salida: Lista de usuarios en formato UserResponse
@router.get("", dependencies=[Depends(required_auth)])
async def get_users(repo: UserRepositoryMongo = Depends(get_collection)) -> list[UserResponse]:
    use_case = ListUsersUseCase(repo)
    users: list[User] = await use_case.execute()
    return users_response(users)

# Endpoint: GET /users/query?key=""&&value=""
# Descripción: Obtiene un usuario filtrando por un campo específico (key, value).
# Requiere autenticación.
# Salida: Usuario en formato UserResponse
@router.get("/query", dependencies=[Depends(required_auth)])
async def get_query(key: str, value: str,
                    repo: UserRepositoryMongo = Depends(get_collection)) -> UserResponse:
    try:
        use_case = GetUserByQueryUseCase(repo)
        user: User = await use_case.execute(key, value)
        return user_response(user)
    except:
        raise EXCEPTION_USER

# Endpoint: GET /users/{id}
# Descripción: Obtiene un usuario por su ID.
# Requiere autenticación.
# Salida: Usuario en formato UserResponse
@router.get("/{id}", dependencies=[Depends(required_auth)])
async def get_by_id(id: str, 
                    repo: UserRepositoryMongo = Depends(get_collection)) -> UserResponse:
    try:
        use_case = GetUserByQueryUseCase(repo)
        # Como es generica la funcion, ingresao el campo 'id' como key, y el valor del id a buscar
        user: User = await use_case.execute("id", id) 
        return user_response(user)
    except:
        raise EXCEPTION_USER

# Endpoint: PUT /users/{id}
# Descripción: Actualizar un usuario por su ID.
# Requiere validacion de id.
# Salida: Objeto Actualizado en formato 'UserResponse'
@router.put("/{id}")#, dependencies=[Depends(required_auth)])
async def update_user(user: UserUpdate,
                      id: str = Depends(user_search), 
                      repo: UserRepositoryMongo = Depends(get_collection)) -> UserResponse:

    use_case = UpdateUserUseCase(repo)
    new_user: User = await use_case.execute(id, user)
    if new_user is None:
        raise EXCEPTION_USER_UPDATE
    return user_response(new_user)

# Endpoint: PATCH /users/{id}?password=""
# Descripción: Actualizar un usuario por su ID.
# Requiere validacion de id.
# Salida: Objeto Actualizado en formato 'UserResponse'
@router.patch("/{id}")
async def update_password(password: str, 
                          id: str = Depends(user_search),
                          repo: UserRepositoryMongo = Depends(get_collection)):
    use_case = UpdatePasswordUserUseCase(repo)
    user: User = await use_case.execute(id, password)

    if user is None:
        raise EXCEPTION_UPDATE_PASSWORD
    return {
        "update": True,
        "detail": "Contraseña actualizada correctamente"
        }

# Endpoint: DELETE /users/{id}
# Descripción: Elimina un usuario por su ID.
# Requiere autenticación.
# Salida: Mensaje de confirmación o excepción si no existe
@router.delete("/{id}", dependencies=[Depends(required_auth)])
async def delete_user(id: str,
                      repo: UserRepositoryMongo = Depends(get_collection)):
    use_case = DeleteUserUseCase(repo)
    condition: bool = await use_case.execute(id)

    if condition is None:
        raise EXCEPTION_USER_DELETE
    return {
        "delete": True,
        "detail": "Usuario eliminado correctamente"
    }