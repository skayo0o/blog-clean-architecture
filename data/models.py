from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from data.db import Base

class UserORM(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    registered_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    posts = relationship("PostORM", back_populates="author")
    comments = relationship("CommentORM", back_populates="author")

class PostORM(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="draft")
    tags = Column(String, default="")  # Сохраняем как строку, например: "tag1,tag2"
    comments_count = Column(Integer, default=0)

    author = relationship("UserORM", back_populates="posts")
    comments = relationship("CommentORM", back_populates="post")

class CommentORM(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_deleted = Column(Boolean, default=False)
    parent_comment_id = Column(Integer, ForeignKey("comments.id"), nullable=True)

    post = relationship("PostORM", back_populates="comments")
    author = relationship("UserORM", back_populates="comments")
    parent_comment = relationship("CommentORM", remote_side=[id])
