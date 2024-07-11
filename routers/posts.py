from fastapi import APIRouter, Depends, HTTPException
from models.modelos import Post, Post_update
from routers.querys import search_post_id, search_post_user
from routers.querys import crear_post, consultar_posts, actualizar_post, eliminar_post
from routers.login import current_user_id

router = APIRouter()


@router.get("/posts")
async def get_posts():

    return consultar_posts()



@router.get("/posts/paginated")
async def get_posts(num_page: int):

    if num_page is None:
        return consultar_posts()
    else:
        saved_posts = consultar_posts()

        limit = 3

        inicio = (num_page - 1) * limit
        final = inicio + limit

        return saved_posts[inicio:final]


@router.get("/posts/me")
async def get_posts(id_current_user: int = Depends(current_user_id)):
    consultar_posts()

    posts_db = search_post_user(id_current_user)

    return posts_db



@router.post("/posts")
async def create_post(post: Post, id_user: int = Depends(current_user_id)):

    try:
        crear_post(post.title, post.content, post.id_category, post.tag, id_user)
        return consultar_posts()
    except:
        raise HTTPException(status_code=304, detail="No se pudo crear el post")
    
    

@router.put("/posts")
async def update_post(post: Post_update, id_user: int = Depends(current_user_id)):

    try:
        actualizar_post(post.id, post.title, post.content, post.id_category, post.tag, id_user)
        return consultar_posts()
    except:
        raise HTTPException(status_code=304, detail="No se pudo actualizar el post")



@router.delete("/posts")
async def delete_post(id_post: int, id_user: int = Depends(current_user_id)):

    saved_post = search_post_id(id_post)

    try:
        if saved_post.id_user == id_user:
            eliminar_post(id_post, id_user)
            return consultar_posts()
        else:
            raise HTTPException(status_code=400, detail="Usted no cuenta con permisos para realizar esta acción")
    except:
        raise HTTPException(status_code=304, detail="El post no pudo ser eliminado")
