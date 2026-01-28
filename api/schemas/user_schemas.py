from pydantic import BaseModel, EmailStr
from Domain.entities.user import User

class UserCreate(BaseModel):
    id: str | None = None
    username: str
    password: str
    email: EmailStr
    age: int

class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    age: int
    
def user_response(user: User) -> UserResponse:
    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        age=user.age
    )
    
def users_response(users: list[User]) -> list[UserResponse]:
    return [user_response(user) for user in users]