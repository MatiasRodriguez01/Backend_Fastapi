# Dependencias necesarias:
# FastAPI:
# - APIRouter: agrupa rutas /users | Depends: inyección de dependencias
# - HTTPException, status: manejo de errores | OAuth2PasswordRequestForm: formulario de login
from fastapi import APIRouter, status, HTTPException, Depends, dependencies
from fastapi.security import OAuth2PasswordRequestForm

# Entidades:
# - UserCreate: modelo de entrada | UserResponse: modelo de salida
# - user_response, users_response: formateo de respuestas
from api.schemas.user_schemas import UserCreate, UserResponse, user_response, users_response

# Casos de uso:
from application.use_cases.GetUserByIdUseCase import GetUserByIdUseCase
from application.use_cases.GetUserByQueryUseCase import GetUserByQueryUseCase
from application.use_cases.ListUsersUseCase import ListUsersUseCase
from application.use_cases.LoginUserUseCase import LoginUserUseCase
from application.use_cases.RegisterUserUseCase import RegisterUserUseCase
from application.use_cases.DeleteUserUseCase import DeleteUserUseCase

# Repositorio:
# - UserRepositoryMongo: acceso a MongoDB | get_user_repository: obtiene repositorio
from infraestructura.repositories.user_repositories_mongo import UserRepositoryMongo
from api.dependencias.GetCollection import  get_user_repository 


# Dependencias Creadas:
# - validate_user_fields: valida datos de usuario
# - required_auth: valida autenticación
from api.dependencias.UserValidate import  validate_user_fields 
from api.dependencias.TokenValidate import  required_auth       

# Seguridad:
# - create_access_token: genera JWT
from infraestructura.security.CreateToken import create_access_token


# Configuración del router de usuarios
# Prefijo: /users
# Tags: users (para documentación automática)
# Respuesta por defecto: 404 si la ruta no existe
router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Ruta no encontrada"}}
)

# Excepción estándar para usuario no encontrado
EXCEPTION_USER = HTTPException(
    status.HTTP_404_NOT_FOUND,
    detail="Usuario no encontrado"
)

# Endpoint: POST /login
# Descripción: Autentica al usuario con username y password.
# Entrada: OAuth2PasswordRequestForm
# Salida: Token JWT de acceso
@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends(),
                repo: UserRepositoryMongo = Depends(get_user_repository)):
    use_case = LoginUserUseCase(repo)
    user = await use_case.execute(form.username, form.password)
    if user:
        return create_access_token(user.username)
    raise EXCEPTION_USER

# Endpoint: POST /register
# Descripción: Registra un nuevo usuario en la base de datos.
# Entrada: UserCreate (username, password, email, age)
# Salida: Token JWT de acceso
@router.post("/register")
async def register(payload: UserCreate = Depends(validate_user_fields),
                   repo: UserRepositoryMongo = Depends(get_user_repository)):
    use_case = RegisterUserUseCase(repo)
    user = await use_case.execute(
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
async def get_users(repo: UserRepositoryMongo = Depends(get_user_repository)) -> list[UserResponse]:
    use_case = ListUsersUseCase(repo)
    users = await use_case.execute()
    return users_response(users)

# Endpoint: GET /users/query
# Descripción: Obtiene un usuario filtrando por un campo específico (key, value).
# Requiere autenticación.
# Salida: Usuario en formato UserResponse
@router.get("/query", dependencies=[Depends(required_auth)])
async def get_query(key: str, value: str,
                    repo: UserRepositoryMongo = Depends(get_user_repository)) -> UserResponse:
    use_case = GetUserByQueryUseCase(repo)
    user = await use_case.execute(key, value)
    if user:
        return user_response(user)
    raise EXCEPTION_USER

# Endpoint: GET /users/{id}
# Descripción: Obtiene un usuario por su ID.
# Requiere autenticación.
# Salida: Usuario en formato UserResponse
@router.get("/{id}", dependencies=[Depends(required_auth)])
async def get_by_id(id: str, repo: UserRepositoryMongo = Depends(get_user_repository)) -> UserResponse:
    use_case = GetUserByIdUseCase(repo)
    user = await use_case.execute(id)
    if user:
        return user_response(user)
    raise EXCEPTION_USER

# Endpoint: DELETE /users/{id}
# Descripción: Elimina un usuario por su ID.
# Requiere autenticación.
# Salida: Mensaje de confirmación o excepción si no existe
@router.delete("/{id}", dependencies=[Depends(required_auth)])
async def delete_user(id: str, repo: UserRepositoryMongo = Depends(get_user_repository)) -> None:
    use_case = DeleteUserUseCase(repo)
    condition = await use_case.execute(id)
    if condition:
        return {"detail": "Usuario eliminado correctamente"}
    else:
        raise EXCEPTION_USER