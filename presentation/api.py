from fastapi import FastAPI, HTTPException, Query, Path, Body
from typing import List, Optional
from presentation.schemas import (
    UserCreate, UserRead,
    PostCreate, PostRead,
    CommentCreate, CommentRead,
)
from data.factories import RepositoryFactory
from domain.services.user_service import UserService
from domain.services.post_service import PostService
from domain.services.comment_service import CommentService
from domain.models.user import User
from domain.models.post import Post
from domain.models.comment import Comment

app = FastAPI(
    title="Blog API",
    description="API для блога с поддержкой пользователей, постов и комментариев. Реализовано по принципам Clean Architecture.",
    version="1.0.0"
)

user_service = UserService(RepositoryFactory.create_user_repository())
post_service = PostService(RepositoryFactory.create_post_repository())
comment_service = CommentService(RepositoryFactory.create_comment_repository())

@app.get(
    "/",
    response_model=dict,
    summary="Корневой маршрут",
    description="Приветственное сообщение и ссылки на документацию."
)
def root():
    """
    Корневой маршрут, возвращающий приветственное сообщение и ссылки на документацию API.
    """
    return {
        "message": "Welcome to the Blog API!",
        "docs_url": "/docs",
        "redoc_url": "/redoc",
    }

@app.post(
    "/users/",
    response_model=UserRead,
    summary="Создать пользователя",
    description="Создаёт нового пользователя. Username и email должны быть уникальными."
)
def create_user(
    user: UserCreate = Body(..., description="Данные нового пользователя")
):
    """
    Создание нового пользователя.
    """
    try:
        created = user_service.create_user(
            User(id=0, username=user.username, email=user.email)
        )
        return UserRead(**created.__dict__)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get(
    "/users/",
    response_model=List[UserRead],
    summary="Список пользователей",
    description="Возвращает список всех пользователей."
)
def list_users():
    """
    Получение списка пользователей.
    """
    users = user_service.list_users()
    return [UserRead(**u.__dict__) for u in users]

@app.get(
    "/users/{user_id}",
    response_model=UserRead,
    summary="Получить пользователя по ID",
    description="Возвращает пользователя по его уникальному идентификатору."
)
def get_user(
    user_id: int = Path(..., description="ID пользователя", example=1)
):
    """
    Получение пользователя по ID.
    """
    user = user_service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserRead(**user.__dict__)

@app.delete(
    "/users/{user_id}",
    status_code=204,
    summary="Удалить пользователя",
    description="Удаляет пользователя по ID. Все связанные посты и комментарии также будут удалены."
)
def delete_user(
    user_id: int = Path(..., description="ID пользователя", example=1)
):
    """
    Удаление пользователя по ID.
    """
    user = user_service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user_service.delete_user(user_id)
    return

@app.post(
    "/posts/",
    response_model=PostRead,
    summary="Создать пост",
    description="Создаёт новый пост. Требуется ID существующего пользователя-автора."
)
def create_post(
    post: PostCreate = Body(..., description="Данные нового поста")
):
    """
    Создание нового поста.
    """
    created = post_service.create_post(
        Post(
            id=0,
            title=post.title,
            content=post.content,
            author_id=post.author_id,
            tags=post.tags or [],
        )
    )
    return PostRead(**created.__dict__)

@app.get(
    "/posts/",
    response_model=List[PostRead],
    summary="Список постов",
    description="Возвращает список всех постов. Можно фильтровать по ID автора."
)
def list_posts(
    author_id: Optional[int] = Query(
        None,
        description="ID автора для фильтрации постов",
        example=1
    )
):
    """
    Получение списка постов с возможностью фильтрации по автору.
    """
    posts = post_service.list_posts(author_id=author_id)
    return [PostRead(**p.__dict__) for p in posts]

@app.get(
    "/posts/{post_id}",
    response_model=PostRead,
    summary="Получить пост по ID",
    description="Возвращает пост по его уникальному идентификатору."
)
def get_post(
    post_id: int = Path(..., description="ID поста", example=1)
):
    """
    Получение поста по ID.
    """
    post = post_service.get_post(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return PostRead(**post.__dict__)

@app.delete(
    "/posts/{post_id}",
    status_code=204,
    summary="Удалить пост",
    description="Удаляет пост по ID. Все связанные комментарии также будут удалены."
)
def delete_post(
    post_id: int = Path(..., description="ID поста", example=1)
):
    """
    Удаление поста по ID.
    """
    post = post_service.get_post(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    post_service.delete_post(post_id)
    return

@app.post(
    "/comments/",
    response_model=CommentRead,
    summary="Создать комментарий",
    description="Создаёт новый комментарий к посту. Можно указать parent_comment_id для вложенных комментариев."
)
def create_comment(
    comment: CommentCreate = Body(..., description="Данные нового комментария")
):
    """
    Создание нового комментария.
    """
    created = comment_service.create_comment(
        Comment(
            id=0,
            post_id=comment.post_id,
            author_id=comment.author_id,
            content=comment.content,
            parent_comment_id=comment.parent_comment_id,
        )
    )
    return CommentRead(**created.__dict__)

@app.get(
    "/comments/",
    response_model=List[CommentRead],
    summary="Список комментариев по посту",
    description="Возвращает список комментариев для указанного поста."
)
def list_comments(
    post_id: int = Query(..., description="ID поста для получения комментариев", example=1)
):
    """
    Получение списка комментариев по ID поста.
    """
    comments = comment_service.list_comments_by_post(post_id)
    return [CommentRead(**c.__dict__) for c in comments]

@app.get(
    "/comments/{comment_id}",
    response_model=CommentRead,
    summary="Получить комментарий по ID",
    description="Возвращает комментарий по его уникальному идентификатору."
)
def get_comment(
    comment_id: int = Path(..., description="ID комментария", example=1)
):
    """
    Получение комментария по ID.
    """
    comment = comment_service.get_comment(comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return CommentRead(**comment.__dict__)

@app.delete(
    "/comments/{comment_id}",
    status_code=204,
    summary="Удалить комментарий",
    description="Удаляет комментарий по ID."
)
def delete_comment(
    comment_id: int = Path(..., description="ID комментария", example=1)
):
    """
    Удаление комментария по ID.
    """
    comment = comment_service.get_comment(comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    comment_service.delete_comment(comment_id)
    return