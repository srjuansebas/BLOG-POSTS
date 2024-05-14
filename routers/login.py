from fastapi import APIRouter, HTTPException, Depends, status, Response, Request
from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from routers.querys import search_user_name, search_user_id, consultar_usuarios
from models.modelos import User_db




# Instanciamos el router
router = APIRouter()

# En esta variable se guarda el token retornado en la ruta "/login"
oauth2 = OAuth2PasswordBearer(tokenUrl="login")

# defino el contexto de encriptación
crypt = CryptContext(schemes=["bcrypt"])

# constante que contiene el algoritmo de encryptacion
ALGORITHM = "HS256"

# la duracion en minutos del token de autenticación
ACCESS_TOKEN_DURATION = 15

# la clave secreta para realizar la encriptación
SECRET = "8bc25bce94c99244fe2e12aa8d84569e145c26b040111b92efb63e57a7b2d7b6"




@router.post("/login")
async def login(response: Response, form: OAuth2PasswordRequestForm = Depends()):
    consultar_usuarios()

    saved_user = search_user_name(form.username)

    if not type(search_user_name(form.username)) == User_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El nombre de usuario ingresado es incorrecto")
    
    if not crypt.verify(form.password, saved_user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña ingresada es incorrecta")
    

    exp = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_DURATION)

    access_token = {
        "exp": exp,
        "sub": saved_user.username,
        "id_user": saved_user.id
    }

    token_encoded = jwt.encode(access_token, SECRET, algorithm=ALGORITHM)

    try:
        response.set_cookie(key="UserToken", value=token_encoded, httponly=True, expires=exp)
        # return {"access_token": token_encoded, "token_type": "bearer"}
        return {"message": "usuario autenticado correctamente"}
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Proceso de inicio de sesion fallido")
    


async def current_user_id(request: Request):
    

    if request.cookies.get("UserToken") is None:
        raise HTTPException(status_code=400, detail="Error de autenticación")
    else:

        cookie_data = request.cookies.get("UserToken")
        token_decoded = jwt.decode(cookie_data, SECRET, algorithms=ALGORITHM)
        id_user = token_decoded.get("id_user")

        
        
        return id_user

