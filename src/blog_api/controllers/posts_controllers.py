from blog_api.db.config import get_connection
import aiomysql as aio
from fastapi import HTTPException, status
from blog_api.models.posts_model import CreatePost, UpdatePost
import json


async def get_all_posts():
    try:
        conn = await get_connection()
        # Abrir y cerrar la conexión de forma segura
        async with conn:
            async with conn.cursor(aio.DictCursor) as cursor:
                await cursor.execute("SELECT * FROM posts")
                post = await cursor.fetchall()
                return post if post else {"msg": "Posts no encontrados"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error: {str(e)}"
        )


async def get_by_id(id: int):
    try:
        conn = await get_connection()
        # Abrir y cerrar la conexión de forma segura
        async with conn:
            async with conn.cursor(aio.DictCursor) as cursor:
                await cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
                post = await cursor.fetchone()
                return post if post else {"msg: Post no encontrado"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error: {str(e)}"
        )


async def create(post: CreatePost):

    # Serializamos el campo tags a JSON en texto antes de pasarlo a la consulta
    tags_json = json.dumps(post.tags) if post.tags is not None else None

    try:
        conn = await get_connection()
        # Abrir y cerrar la conexión de forma segura
        async with conn:
            async with conn.cursor(aio.DictCursor) as cursor:
                # Reutilizamos la función pasando el cursor y el título
                await validate_unique_title(cursor, post.title)

                # Si el título no está duplicado, continúa la ejecución
                await cursor.execute(
                    "INSERT INTO posts(title, content, category, tags) VALUES (%s, %s, %s, %s)",
                    (post.title, post.content, post.category, tags_json),
                )
                await conn.commit()
                new_id = cursor.lastrowid
                post = await get_by_id(new_id)
                return {"msg": "Post creado correctamente", "item": post}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error: {str(e)}"
        )


async def update(id: int, post: UpdatePost):
    # Serializamos el campo tags a JSON en texto antes de pasarlo a la consulta
    tags_json = json.dumps(post.tags) if post.tags is not None else None

    try:
        conn = await get_connection()
        # Abrir y cerrar la conexión de forma segura
        async with conn:
            async with conn.cursor(aio.DictCursor) as cursor:
                await cursor.execute(
                    "UPDATE posts SET title = %s, content = %s, category = %s, tags = %s WHERE id = %s",
                    (post.title, post.content, post.category, tags_json, post.id),
                )

                if cursor.rowcount == 0:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="El post que quieres actualizar no existe",
                    )

                await conn.commit()
                return {
                    "msg": "Post actualizado correctamente",
                    "post": await get_by_id(id),
                }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error: {str(e)}"
        )


async def delete(id: int):
    try:
        conn = await get_connection()
        # Abrir y cerrar la conexión de forma segura
        async with conn:
            async with conn.cursor(aio.DictCursor) as cursor:
                await cursor.execute("DELETE FROM posts WHERE id=%s", (id,))

                if cursor.rowcount == 0:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="El post que quieres borrar no existe",
                    )

                await conn.commit()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error: {str(e)}"
        )


async def is_title_taken(cursor: aio.DictCursor, title: str) -> bool:
    # Consulta la BD para comprobar si el título ya está en uso.
    await cursor.execute(
        "SELECT 1 FROM posts WHERE LOWER(title) = LOWER(%s) LIMIT 1",
        (title.strip(),),
    )
    return await cursor.fetchone() is not None


async def validate_unique_title(cursor: aio.DictCursor, title: str) -> None:
    # Lanza un error 400 si el título ya existe en la BD.
    if await is_title_taken(cursor, title):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe una publicación con el título: '{title}'",
        )
