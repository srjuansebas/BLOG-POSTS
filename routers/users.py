from fastapi import APIRouter, HTTPException, Depends, Response, Cookie, Request
from typing import Annotated
from models.modelos import User, User_db
from routers.querys import search_user_name, search_user_id
from routers.querys import crear_usuario, consultar_usuarios, actualizar_usuario, admin_actualizar_usuario, eliminar_usuario
from routers.login import current_user
from fastapi.responses import RedirectResponse
from jose import jwt 

router = APIRouter()


ALGORITHM = "HS256"

# la duracion en minutos del token de autenticación
ACCESS_TOKEN_DURATION = 5

# la clave secreta para realizar la encriptación
SECRET = "8bc25bce94c99244fe2e12aa8d84569e145c26b040111b92efb63e57a7b2d7b6"

@router.get("/users")
async def get_users():
    return consultar_usuarios()

@router.get("/users/me")
async def get_current_user(user: User_db = Depends(current_user)):
    
    return user 

    # if request.cookies.get("UserToken") is None:
    #     raise HTTPException(status_code=400, detail="Error de autenticación")
    # else:

    #     cookie_data = request.cookies.get("UserToken")
    #     token_decoded = jwt.decode(cookie_data, SECRET, algorithms=ALGORITHM)
    #     id_user = token_decoded.get("id_user")

    #     saved_user = search_user_id(id_user)
        
    #     return saved_user

@router.post("/users")
async def create_user(user: User):

    if type(search_user_name(user.username)) == User_db:
        raise HTTPException(status_code=400, detail="El usuario ya esta registrado")
    
    try:
        crear_usuario(user.username, user.email, user.password)
        return consultar_usuarios()
    except:
        raise HTTPException(status_code=304, detail="El usuario no pudo ser registrado")

@router.put("/users")
async def update_user(user: User_db, current_user: User_db = Depends(current_user)):

    if not type(search_user_id(user.id)) == User_db:
        raise HTTPException(status_code=400, detail="El usuario no ha sido registrado")
    
    try:
        if current_user.role == "administrador":
            admin_actualizar_usuario(user.id, user.username, user.email, user.password, user.role)
            return consultar_usuarios()
        else:
            actualizar_usuario(user.id, user.username, user.email, user.password)
            return consultar_usuarios()
    except:
        raise HTTPException(status_code=304, detail="El usuario no pudo ser actualizado")
    


@router.delete("/users/{id}")
async def delete_user(id: int, current_user: User_db = Depends(current_user)):

    if not type(search_user_id(id)) == User_db:
        raise HTTPException(status_code=400, detail="El usuario no está registrado")
    
    try:
        if current_user.role == "administrador":
            eliminar_usuario(id)
            return RedirectResponse("/", status_code=302)
        else:
            raise HTTPException(status_code=400, detail="Usted no cuenta con permisos para realizar esta acción")
    except:
        raise HTTPException(status_code=304, detail="El usuario no pudo ser eliminado")
