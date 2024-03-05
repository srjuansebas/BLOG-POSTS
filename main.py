from fastapi import FastAPI
from routers.querys import consultar_usuarios

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Bienvenido a tu BLOG"}



@app.get("/users")
async def get_users():
    return consultar_usuarios()