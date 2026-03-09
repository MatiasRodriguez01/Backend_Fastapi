from fastapi import FastAPI, Depends, dependencies
from api.routers import authentication, users

from api.dependencias.TokenValidate import required_auth

app = FastAPI()

app.include_router(authentication.router)
app.include_router(users.router)
