from typing import List, Optional
from domain.models.comment import Comment
from domain.repositories.comment_repository import CommentRepository

class CommentService:
    def __init__(self, comment_repository: CommentRepository):
        self.comment_repository = comment_repository

    def get_comment(self, comment_id: int) -> Optional[Comment]:
        return self.comment_repository.get_by_id(comment_id)

    def list_comments_by_post(self, post_id: int) -> List[Comment]:
        return self.comment_repository.list_by_post(post_id)

    def create_comment(self, comment: Comment) -> Comment:
        return self.comment_repository.create(comment)

    def update_comment(self, comment: Comment) -> Comment:
        return self.comment_repository.update(comment)

    def delete_comment(self, comment_id: int) -> None:
        self.comment_repository.delete(comment_id)
