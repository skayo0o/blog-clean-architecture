from sqlalchemy.orm import Session
from typing import List, Optional
from domain.models.comment import Comment
from domain.repositories.comment_repository import CommentRepository
from data.models import CommentORM
from data.db import SessionLocal

class CommentRepositoryImpl(CommentRepository):
    def __init__(self, db_session: Optional[Session] = None):
        self.db: Session = db_session or SessionLocal()

    def get_by_id(self, comment_id: int) -> Optional[Comment]:
        comment = self.db.query(CommentORM).filter(CommentORM.id == comment_id).first()
        return self._to_domain(comment) if comment else None

    def list_by_post(self, post_id: int) -> List[Comment]:
        comments = self.db.query(CommentORM).filter(CommentORM.post_id == post_id).all()
        return [self._to_domain(c) for c in comments]

    def create(self, comment: Comment) -> Comment:
        comment_orm = CommentORM(
            post_id=comment.post_id,
            author_id=comment.author_id,
            content=comment.content,
            created_at=comment.created_at,
            is_deleted=comment.is_deleted,
            parent_comment_id=comment.parent_comment_id,
        )
        self.db.add(comment_orm)
        self.db.commit()
        self.db.refresh(comment_orm)
        return self._to_domain(comment_orm)

    def update(self, comment: Comment) -> Comment:
        comment_orm = self.db.query(CommentORM).filter(CommentORM.id == comment.id).first()
        if not comment_orm:
            raise ValueError("Comment not found")
        comment_orm.content = comment.content
        comment_orm.is_deleted = comment.is_deleted
        comment_orm.parent_comment_id = comment.parent_comment_id
        self.db.commit()
        self.db.refresh(comment_orm)
        return self._to_domain(comment_orm)

    def delete(self, comment_id: int) -> None:
        comment_orm = self.db.query(CommentORM).filter(CommentORM.id == comment_id).first()
        if comment_orm:
            self.db.delete(comment_orm)
            self.db.commit()

    def _to_domain(self, comment_orm: CommentORM) -> Comment:
        return Comment(
            id=comment_orm.id,
            post_id=comment_orm.post_id,
            author_id=comment_orm.author_id,
            content=comment_orm.content,
            created_at=comment_orm.created_at,
            is_deleted=comment_orm.is_deleted,
            parent_comment_id=comment_orm.parent_comment_id,
        )