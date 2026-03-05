from fastapi import FastAPI, Depends, dependencies
from api.routers import authentication, users
from jose import ExpiredSignatureError

from api.dependecias import required_auth

app = FastAPI()

app.include_router(authentication.router)
app.include_router(users.router)

@app.get("/privada", dependencies = [Depends(required_auth)])
async def ruta_privada():
    return {"ok": True, "msg": "Entraste porque estabas autenticado"}