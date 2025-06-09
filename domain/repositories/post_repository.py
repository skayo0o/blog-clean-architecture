from abc import ABC, abstractmethod
from typing import List, Optional
from domain.models.post import Post

class PostRepository(ABC):
    @abstractmethod
    def get_by_id(self, post_id: int) -> Optional[Post]:
        pass

    @abstractmethod
    def list(self, author_id: Optional[int] = None) -> List[Post]:
        pass

    @abstractmethod
    def create(self, post: Post) -> Post:
        pass

    @abstractmethod
    def update(self, post: Post) -> Post:
        pass

    @abstractmethod
    def delete(self, post_id: int) -> None:
        pass
