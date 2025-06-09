from typing import List, Optional
from domain.models.post import Post
from domain.repositories.post_repository import PostRepository

class PostService:
    def __init__(self, post_repository: PostRepository):
        '''
        Инициализация сервиса постов.
        '''
        if not isinstance(post_repository, PostRepository):
            raise TypeError("post_repository must be an instance of PostRepository")
        self.post_repository = post_repository

    def get_post(self, post_id: int) -> Optional[Post]:
        '''
        Получение поста по ID.
        '''
        if post_id <= 0:
            raise ValueError("Post ID must be a positive integer")
        return self.post_repository.get_by_id(post_id)

    def list_posts(self, author_id: Optional[int] = None) -> List[Post]:
        '''
        Получение списка постов, возможно, отфильтрованного по автору.
        '''
        if author_id is not None and author_id <= 0:
            raise ValueError("Author ID must be a positive integer")
        return self.post_repository.list(author_id=author_id)

    def create_post(self, post: Post) -> Post:
        '''
        Создание нового поста.
        '''
        if not post.title or not post.content:
            raise ValueError("Post title and content cannot be empty")
        return self.post_repository.create(post)

    def update_post(self, post: Post) -> Post:
        '''
        Обновление информации о посте.
        '''
        if post.id <= 0:
            raise ValueError("Post ID must be a positive integer")
        return self.post_repository.update(post)

    def delete_post(self, post_id: int) -> None:
        '''
        Удаление поста по ID.
        '''
        if post_id <= 0:
            raise ValueError("Post ID must be a positive integer")
        self.post_repository.delete(post_id)
