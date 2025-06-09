from fastapi import FastAPI, HTTPException, Query
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

app = FastAPI()

# Используем фабрику для создания репозиториев
user_service = UserService(RepositoryFactory.create_user_repository())
post_service = PostService(RepositoryFactory.create_post_repository())
comment_service = CommentService(RepositoryFactory.create_comment_repository())

@app.get("/", response_model=dict)
def root():
    '''
    Корневой маршрут, возвращающий приветственное сообщение и ссылки на документацию.
    '''
    return {
        "message": "Welcome to the Blog API!",
        "docs_url": "/docs",
        "redoc_url": "/redoc",
    }

@app.post("/users/", response_model=UserRead)
def create_user(user: UserCreate):
    '''
    Создание нового пользователя.
    '''
    try:
        created = user_service.create_user(
            User(id=0, username=user.username, email=user.email)
        )
        return UserRead(**created.__dict__)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/users/", response_model=List[UserRead])
def list_users():
    '''
    Получение списка пользователей.
    '''
    users = user_service.list_users()
    return [UserRead(**u.__dict__) for u in users]

@app.get("/users/{user_id}", response_model=UserRead)
def get_user(user_id: int):
    '''
    Получение пользователя по ID.
    '''
    user = user_service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserRead(**user.__dict__)

@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int):
    '''
    Удаление пользователя по ID.
    '''
    user = user_service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user_service.delete_user(user_id)
    return

@app.post("/posts/", response_model=PostRead)
def create_post(post: PostCreate):
    '''
    Создание нового поста.
    '''
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

@app.get("/posts/", response_model=List[PostRead])
def list_posts(author_id: Optional[int] = Query(None)):
    '''
    Получение списка постов с возможностью фильтрации по автору.
    '''
    posts = post_service.list_posts(author_id=author_id)
    return [PostRead(**p.__dict__) for p in posts]

@app.get("/posts/{post_id}", response_model=PostRead)
def get_post(post_id: int):
    '''
    Получение поста по ID.
    '''
    post = post_service.get_post(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return PostRead(**post.__dict__)

@app.delete("/posts/{post_id}", status_code=204)
def delete_post(post_id: int):
    '''
    Удаление поста по ID.
    '''
    post = post_service.get_post(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    post_service.delete_post(post_id)
    return

@app.post("/comments/", response_model=CommentRead)
def create_comment(comment: CommentCreate):
    '''
    Создание нового комментария.
    '''
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

@app.get("/comments/", response_model=List[CommentRead])
def list_comments(post_id: int = Query(...)):
    '''
    Получение списка комментариев по ID поста.
    '''
    comments = comment_service.list_comments_by_post(post_id)
    return [CommentRead(**c.__dict__) for c in comments]

@app.get("/comments/{comment_id}", response_model=CommentRead)
def get_comment(comment_id: int):
    '''
    Получение комментария по ID.
    '''
    comment = comment_service.get_comment(comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return CommentRead(**comment.__dict__)

@app.delete("/comments/{comment_id}", status_code=204)
def delete_comment(comment_id: int):
    '''
    Удаление комментария по ID.
    '''
    comment = comment_service.get_comment(comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    comment_service.delete_comment(comment_id)
    return