from typing import List, Optional
from domain.models.comment import Comment
from domain.repositories.comment_repository import CommentRepository

class CommentService:
    def __init__(self, comment_repository: CommentRepository):
        '''
        Инициализация сервиса комментариев.
        '''
        if not isinstance(comment_repository, CommentRepository):
            raise TypeError("comment_repository must be an instance of CommentRepository")
        self.comment_repository = comment_repository

    def get_comment(self, comment_id: int) -> Optional[Comment]:
        '''
        Получение комментария по ID.
        '''
        return self.comment_repository.get_by_id(comment_id)

    def list_comments_by_post(self, post_id: int) -> List[Comment]:
        '''
        Получение списка комментариев по ID поста.
        '''
        if post_id <= 0:
            raise ValueError("Post ID must be a positive integer")
        return self.comment_repository.list_by_post(post_id)

    def create_comment(self, comment: Comment) -> Comment:
        '''
        Создание нового комментария.
        '''
        if not comment.content or comment.post_id <= 0:
            raise ValueError("Comment content cannot be empty and post ID must be a positive integer")
        return self.comment_repository.create(comment)

    def update_comment(self, comment: Comment) -> Comment:
        '''
        Обновление информации о комментарии.
        '''
        if comment.id <= 0:
            raise ValueError("Comment ID must be a positive integer")
        return self.comment_repository.update(comment)

    def delete_comment(self, comment_id: int) -> None:
        '''
        Удаление комментария по ID.
        '''
        if comment_id <= 0:
            raise ValueError("Comment ID must be a positive integer")
        self.comment_repository.delete(comment_id)
