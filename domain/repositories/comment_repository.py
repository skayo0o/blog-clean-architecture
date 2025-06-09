from abc import ABC, abstractmethod
from typing import List, Optional
from domain.models.comment import Comment

class CommentRepository(ABC):
    @abstractmethod
    def get_by_id(self, comment_id: int) -> Optional[Comment]:
        pass

    @abstractmethod
    def list_by_post(self, post_id: int) -> List[Comment]:
        pass

    @abstractmethod
    def create(self, comment: Comment) -> Comment:
        pass

    @abstractmethod
    def update(self, comment: Comment) -> Comment:
        pass

    @abstractmethod
    def delete(self, comment_id: int) -> None:
        pass