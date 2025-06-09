from typing import List, Optional
from domain.models.user import User
from domain.repositories.user_repository import UserRepository

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def get_user(self, user_id: int) -> Optional[User]:
        return self.user_repository.get_by_id(user_id)

    def get_user_by_username(self, username: str) -> Optional[User]:
        return self.user_repository.get_by_username(username)

    def list_users(self) -> List[User]:
        return self.user_repository.list()

    def create_user(self, user: User) -> User:
        # Проверка уникальности username/email
        if self.user_repository.get_by_username(user.username):
            raise ValueError("Username already exists")
        return self.user_repository.create(user)

    def update_user(self, user: User) -> User:
        return self.user_repository.update(user)

    def delete_user(self, user_id: int) -> None:
        self.user_repository.delete(user_id)