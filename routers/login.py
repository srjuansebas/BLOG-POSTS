from typing import Coroutine
from fastapi import APIRouter, HTTPException, Depends, status, Response, Request
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from routers.querys import search_user_name, search_user_id, consultar_usuarios
from models.modelos import User_db
from starlette.middleware.base import BaseHTTPMiddleware


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






# class ExtendTokenExpire(BaseHTTPMiddleware):

#     def dispatch(self, request: Request, call_next):

#         cookie_data = request.cookies.get("UserToken")

#         if cookie_data:
#             try:

#                 token_decoded = jwt.decode(cookie_data, SECRET, algorithms=[ALGORITHM])
#                 new_exp = datetime.now(timezone.utc) + timedelta(minutes=5)
#                 token_decoded["exp"] = new_exp

#                 new_token = jwt.encode(token_decoded, SECRET, algorithm=ALGORITHM)

#                 request.state.new_token = new_token

#             except JWTError:
#                 pass

#         response = await call_next(request)

#         if hasattr(request.state, "new_token"):
#             response.set_cookie(key="UserToken", value=request.state.new_token, httponly=True, expires=new_exp)

#         return response




class ExtendTokenExpire(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):


        # Obtenemos el token almacenado en la cookie "UserToken"
        token_cookie = request.cookies.get("UserToken")

        if token_cookie:  # Verificamos que haya contenido en la cookie
            try:
                # Decodificar el token
                token_decoded = jwt.decode(token_cookie, SECRET, algorithms=[ALGORITHM])

                # Extender el tiempo de expiración
                new_exp = datetime.now(timezone.utc) + timedelta(minutes=5)
                token_decoded["exp"] = new_exp

                # Volver a codificar el token
                new_token = jwt.encode(token_decoded, SECRET, algorithm=ALGORITHM)

                # Para actualizar la cookie con el token

                # eliminamos la cookie
                response.delete_cookie("UserToken")
                # Asignamos nuevamente la cookie con el nuevo contenido
                response.set_cookie(key="UserToken", value=new_token, httponly=True, expires=new_exp)
            except JWTError:
                pass  # Si hay un error en la decodificación, no hacer nada

        response = await call_next(request)

        # if hasattr(request.state, "new_token"):
            # response.set_cookie(key="UserToken", value=new_token, httponly=True, expires=new_exp)

        return response





@router.post("/login")
async def login(response: Response, request: Request, form: OAuth2PasswordRequestForm = Depends()):
    consultar_usuarios()


    # if request.cookies.get("UserToken"):    
    #     response.headers.append("Set-Cookie", "UserToken=; Max-Age=0")
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
        return {"message": "usuario autenticado correctamente"}
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Proceso de inicio de sesion fallido")
    


async def current_user_id(request: Request):
    
    if request.cookies.get("UserToken") is None:
        raise HTTPException(status_code=400, detail="Error de autenticación")
    else:
        cookie_data = request.cookies.get("UserToken")
        token_decoded = jwt.decode(cookie_data, SECRET, algorithms=[ALGORITHM])
        id_user = token_decoded.get("id_user")
        return id_user



@router.delete("logout")
async def logout(response: Response):
    response.delete_cookie("UserToken")
    return {"message": "hasta luego, vuelve pronto"}


@router.get("/users/me")
async def get_current_user(id_user: int = Depends(current_user_id)):
    
    saved_user = search_user_id(id_user)

    return saved_user 