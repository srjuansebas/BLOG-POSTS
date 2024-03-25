from fastapi import APIRouter, HTTPException, Depends
from models.modelos import User, User_db
from routers.querys import consultar_usuarios, search_user_name, search_user_id, crear_usuario, actualizar_usuario, admin_actualizar_usuario, eliminar_usuario
from routers.login import current_user, current_user_id


router = APIRouter()


@router.get("/users")
async def get_users():
    return consultar_usuarios()

@router.get("/users/me")
async def get_current_user(user: User_db = Depends(current_user)):

    return user

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
