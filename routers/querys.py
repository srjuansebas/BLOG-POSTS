from models.modelos import User, User_db, Post, Post_db, Post_show, Comment, Comment_db
import mysql.connector


# Instanciando la conexion a la base de datos
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="main",
    database="blog_post",
    port=3306
)


# creando el cursor para ejecutar las consultas
cursor = conexion.cursor()


# En estas listas almacenaremos los datos temporalmente al obtenerlos
users_db = []

posts_db = []

comments_db = []


# creando las funciones para obtener los datos


def consultar_usuarios():

    users_db.clear()
    cursor.execute("SELECT * FROM users")

    for id, username, email, password, role, in cursor.fetchall():
        users_db.append(User_db(id=id, username=username, email=email, password=password, role=role))

    return users_db

def consultar_posts():

    posts_db.clear()
    cursor.execute("SELECT * FROM posts")

    for id, title, content, date, hour, id_category, tag, id_user in  cursor.fetchall():
        posts_db.append(Post_db(id=id, title=title, content=content, date=date, hour=hour, id_category=id_category, tag=tag, id_user=id_user))

    return posts_db


def consultar_comentarios():

    comments_db.clear()
    cursor.execute("SELECT * FROM comments")

    for id, content, id_post, id_user, date in cursor.fetchall():
        comments_db.append(Comment_db(id=id, content=content, id_post=id_post, id_user=id_user, date=date))

    return comments_db



# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# iniciando a crear las operaciones para trabajar con los usuarios en la base de datos



def search_user_id(id: int):

    users = filter(lambda user: user.id == id, users_db)

    try:
        return users[0]
    except:
        return {"error": "No se ha encontrado el usuario"}
    

def search_user_name(username: str):
    users = filter(lambda user: user.username == username, users_db)

    try:
        return users[0]
    except:
        return {"error": "No se ha encontrado el usuario"}
    
# --------------------------------------------------------------------------------------------------------------------------------------------

def crear_usuario(username: str, email: str, password: str):

    try:
        cursor.execute(f"INSERT INTO users (nombre_usuario, correo, contraseña) VALUES ({username}, {email}, {password})")
        conexion.commit()
    except:
        return {"error": "No se pudo crear el nuevo usuario"}
    
# -------------------------------------------------------------------------------------------------------------------------------------------

def actualizar_usuario(id: int, username: str, email: str, password: str, role: str):

    try:
        cursor.execute(f"UPDATE users SET nombre_usuario='{username}', correo='{email}', contraseña='{password}', rol='{role}' WHERE id={id}")
        conexion.commit()
    except:
        return {"error": "No se pudo actualizar el usuario"}
    

# ----------------------------------------------------------------------------------------------------------------------------------------

def eliminar_usuario(id: int):
    
    try:
        cursor.execute(f"DELETE FROM users WHERE id={id}")
        conexion.commit()
    except:
        return {"error": "No se pudo eliminar el usuario"}
    


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# definiendo las operaciones para trabajar con los posts en la base de datos
    

def crear_post(title: str, content: str, category_id: int, tag: str, id_user: int):

    try:
        cursor.execute(f"INSERT INTO posts (titulo, contenido, fecha, hora, id_categoria, etiqueta, id_usuario) VALUES ('{title}', '{content}', curdate(), date_format(now(), '%H:%i:%S'), {category_id}, '{tag}', {id_user})")
        conexion.commit()
    except:
        return {"error": "No se pudo postear"}
    

def actualizar_post(id: int, title: str, content: str, category_id: int, tag: str, id_user: int):

    try:
        cursor.execute(f"UPDATE posts SET title='{title}', content='{content}', id_categoria='{category_id}', etiqueta='{tag}' WHERE id={id} and id_usuario={id_user}")
        conexion.commit()
    except:
        return {"error": "No se pudo actualizar el post"}
    

def eliminar_post(id: int):

    try:
        cursor.execute(f"DELETE FROM posts WHERE id={id}")
        conexion.commit()
    except:
        return {"error": "No se pudo eliminar el post"}
    


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# definiendo las operaciones para trabajar con los comentarios en la base de datos


def crear_comentario(content: str, id_post: int, id_user: int):

    try:
        cursor.execute(f"INSERT INTO comments (contenido, id_post, id_usuario, fecha) VALUES ('{content}', {id_post}, {id_user}, curdate())")
        conexion.commit()
    except:
        return {"error": "No se pudo hacer el comentario"}
    


def actualizar_comentario(id: int, content: str, id_post: int, id_user: int):

    try:
        cursor.execute(f"UPDATE comments SET contenido='{content}' WHERE id={id} and id_user={id_user} and id_post={id_post}")
        conexion.commit()
    except:
        return {"error": "No se pudo actualizar el comentario"}



def eliminar_comentario(id: int):

    try:
        cursor.execute(f"DELETE FROM commets WHERE id={id}")
        conexion.commit()
    except:
        return {"error": "No se pudo eliminar el comentario"}