from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from api.schemas.user_schemas import UserCreate, UserResponse, user_response, users_response
from aplicacion.use_cases.login_user import LoginUserUseCase
from aplicacion.use_cases.create_user import CreateUserUseCase
from infraestructura.repositories.user_repositories_mongo import UserRepositoryMongo
from aplicacion.security.jwt_handler import create_access_token


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "No Funciona la Ruta usersTest"}},)


@router.get("", response_model=list[UserResponse])
async def get_users():
    repo = UserRepositoryMongo()
    use_case = CreateUserUseCase(repo)

    return users_response(use_case.users())

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    repo = UserRepositoryMongo()
    use_case = LoginUserUseCase(repo)
    
    user = use_case.login(form.username, form.password)
    
    return create_access_token(user.username)

@router.post("/register")
async def register(payload: UserCreate):
    repo = UserRepositoryMongo()
    use_case = CreateUserUseCase(repo)

    user = use_case.register(
        username=payload.username,
        password=payload.password,
        email=payload.email,
        age=payload.age
    )

    return create_access_token(user.username)

@router.get("/{username}", response_model=UserResponse)
async def get_user(username: str):
    repo = UserRepositoryMongo()
    use_case = CreateUserUseCase(repo)

    user = use_case.show_user(username)

    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

    return user_response(user)
