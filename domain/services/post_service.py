from typing import List, Optional
from domain.models.post import Post
from domain.repositories.post_repository import PostRepository

class PostService:
    def __init__(self, post_repository: PostRepository):
        self.post_repository = post_repository

    def get_post(self, post_id: int) -> Optional[Post]:
        return self.post_repository.get_by_id(post_id)

    def list_posts(self, author_id: Optional[int] = None) -> List[Post]:
        return self.post_repository.list(author_id=author_id)

    def create_post(self, post: Post) -> Post:
        return self.post_repository.create(post)

    def update_post(self, post: Post) -> Post:
        return self.post_repository.update(post)

    def delete_post(self, post_id: int) -> None:
        self.post_repository.delete(post_id)