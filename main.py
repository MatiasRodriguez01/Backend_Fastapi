from fastapi import FastAPI
from routers import users, products, authentication

app = FastAPI()

app.include_router(users.router)
app.include_router(products.router)
app.include_router(authentication.router)

@app.get("/")
async def root():
    return "¡¡HOLA MundoOOO!!"