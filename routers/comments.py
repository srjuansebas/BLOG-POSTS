from fastapi import APIRouter, Depends, HTTPException
from models.modelos import Comment, Comment_update
from routers.querys import consultar_comentarios, search_comment_id, search_comment_post
from routers.querys import crear_comentario, actualizar_comentario, eliminar_comentario
from routers.login import current_user_id





router = APIRouter()


@router.get("/comments")
async def get_comments():
    
    return consultar_comentarios()

@router.get("/comments/post/{id_post}")
async def get_comment_post(id_post: int):

    return search_comment_post(id_post)


@router.post("/comments")
async def create_comment(comment: Comment, id_post: int, current_user_id: int = Depends(current_user_id)):

    try:
        crear_comentario(comment.content, id_post, current_user_id)
        return consultar_comentarios()
    except:
        raise HTTPException(status_code=304, detail="No se pudo crear el comentario")
    


@router.put("/comments")
async def update_comments(comment: Comment_update, id_user: int = Depends(current_user_id)):
    
    try:
        actualizar_comentario(comment.id, comment.content, comment.id_post, id_user)
        return search_comment_id(comment.id)
    except:
        raise HTTPException(status_code=304, detail="No se pudo actualizar el comentario")

@router.delete("/comments/{id}")
async def delete_comment(id: int):

    try:
        eliminar_comentario(id)
        return {"message": "Comentario eliminado exitosamente"}
    except:
        raise HTTPException(status_code=304, detail="No se pudo eliminar el comentario")