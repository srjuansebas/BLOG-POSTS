from fastapi import APIRouter
from models.modelos import User, User_db
from routers.querys import consultar_usuarios

router = APIRouter()


@router.get("/users")
async def get_users():
    return consultar_usuarios()



