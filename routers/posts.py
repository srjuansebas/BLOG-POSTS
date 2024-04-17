from fastapi import APIRouter, Depends, status, HTTPException
from models.modelos import Post, Post_db, Post_show, User_db
from routers.querys import search_post_title, search_post_id
from routers.querys import crear_post, consultar_posts, actualizar_post, eliminar_post
from routers.login import current_user

router = APIRouter()


@router.get("/posts")
async def get_posts():

    return consultar_posts()

@router.post("/posts")
async def create_post(post: Post, user: User_db = Depends(current_user)):

    try:
        crear_post(post.title, post.content, post.id_category, post.tag, user.id)
        return consultar_posts()
    except:
        raise HTTPException(status_code=304, detail="No se pudo crear el post")
    
