from sqlalchemy.orm import Session
from typing import List, Optional
from domain.models.post import Post
from domain.repositories.post_repository import PostRepository
from data.models import PostORM
from data.db import SessionLocal

class PostRepositoryImpl(PostRepository):
    def __init__(self, db_session: Optional[Session] = None):
        self.db: Session = db_session or SessionLocal()

    def get_by_id(self, post_id: int) -> Optional[Post]:
        post = self.db.query(PostORM).filter(PostORM.id == post_id).first()
        return self._to_domain(post) if post else None

    def list(self, author_id: Optional[int] = None) -> List[Post]:
        query = self.db.query(PostORM)
        if author_id is not None:
            query = query.filter(PostORM.author_id == author_id)
        posts = query.all()
        return [self._to_domain(p) for p in posts]

    def create(self, post: Post) -> Post:
        post_orm = PostORM(
            title=post.title,
            content=post.content,
            author_id=post.author_id,
            created_at=post.created_at,
            status=post.status,
            tags=",".join(post.tags),
            comments_count=post.comments_count,
        )
        self.db.add(post_orm)
        self.db.commit()
        self.db.refresh(post_orm)
        return self._to_domain(post_orm)

    def update(self, post: Post) -> Post:
        post_orm = self.db.query(PostORM).filter(PostORM.id == post.id).first()
        if not post_orm:
            raise ValueError("Post not found")
        post_orm.title = post.title
        post_orm.content = post.content
        post_orm.status = post.status
        post_orm.tags = ",".join(post.tags)
        post_orm.comments_count = post.comments_count
        self.db.commit()
        self.db.refresh(post_orm)
        return self._to_domain(post_orm)

    def delete(self, post_id: int) -> None:
        post_orm = self.db.query(PostORM).filter(PostORM.id == post_id).first()
        if post_orm:
            self.db.delete(post_orm)
            self.db.commit()

    def _to_domain(self, post_orm: PostORM) -> Post:
        return Post(
            id=post_orm.id,
            title=post_orm.title,
            content=post_orm.content,
            author_id=post_orm.author_id,
            created_at=post_orm.created_at,
            status=post_orm.status,
            tags=post_orm.tags.split(",") if post_orm.tags else [],
            comments_count=post_orm.comments_count,
        )