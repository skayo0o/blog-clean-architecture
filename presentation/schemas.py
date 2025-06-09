from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr

class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    registered_at: datetime
    is_active: bool

    class Config:
        model_config = {"from_attributes": True}

class PostCreate(BaseModel):
    title: str
    content: str
    author_id: int
    tags: Optional[List[str]] = []

class PostRead(BaseModel):
    id: int
    title: str
    content: str
    author_id: int
    created_at: datetime
    status: str
    tags: List[str]
    comments_count: int

    class Config:
        model_config = {"from_attributes": True}

class CommentCreate(BaseModel):
    post_id: int
    author_id: int
    content: str
    parent_comment_id: Optional[int] = None

class CommentRead(BaseModel):
    id: int
    post_id: int
    author_id: int
    content: str
    created_at: datetime
    is_deleted: bool
    parent_comment_id: Optional[int]

    class Config:
        model_config = {"from_attributes": True}
