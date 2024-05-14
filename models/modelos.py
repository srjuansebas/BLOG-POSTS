from pydantic import BaseModel
from typing import Optional




# creando las clases del usuario
class User(BaseModel):
    username: str
    email: Optional[str] = "Sin email disponible..."
    password: str



class User_db(BaseModel):
    id: int
    username: str
    email: Optional[str] = "Sin email disponible..."
    password: str
    role: str

# -----------------------------------------------------------------------------------

# creando las clases de los posts
class Post(BaseModel):
    title: str
    content: Optional[str] = "Sin contenido..."
    id_category: int
    tag: str


class Post_update(BaseModel):
    id: int
    title: str
    content: Optional[str] = "Sin contenido..."
    id_category: int
    tag: str
    


class Post_db(BaseModel):
    id: int
    title: str
    content: Optional[str] = "Sin contenido..."
    date: str
    hour: str
    id_category: int
    tag: str
    id_user: int
    

# -----------------------------------------------------------------------------------

# creando las clases de los comentarios

class Comment(BaseModel):
    content: str

class Comment_update(BaseModel):
    id: int
    content: str
    id_post: int


class Comment_db(BaseModel):
    id: int
    content: str
    id_post: int
    id_user: int
    date: str

