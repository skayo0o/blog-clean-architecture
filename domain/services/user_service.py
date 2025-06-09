from typing import List, Optional
from domain.models.user import User
from domain.repositories.user_repository import UserRepository

class UserService:
    def __init__(self, user_repository: UserRepository):
        '''
        Инициализация сервиса пользователей.
        '''
        self.user_repository = user_repository

    def get_user(self, user_id: int) -> Optional[User]:
        '''
        Получение пользователя по ID.
        '''
        if user_id <= 0:
            raise ValueError("User ID must be a positive integer")
        return self.user_repository.get_by_id(user_id)

    def get_user_by_username(self, username: str) -> Optional[User]:
        '''
        Получение пользователя по username.
        '''
        if not username:
            raise ValueError("Username cannot be empty")
        return self.user_repository.get_by_username(username)

    def list_users(self) -> List[User]:
        '''
        Получение списка всех пользователей.
        '''
        if not self.user_repository.list():
            raise ValueError("No users found")
        return self.user_repository.list()

    def create_user(self, user: User) -> User:
        '''
        Создание нового пользователя.
        '''
        if self.user_repository.get_by_username(user.username):
            raise ValueError("Username already exists")
        return self.user_repository.create(user)

    def update_user(self, user: User) -> User:
        '''
        Обновление информации о пользователе.
        '''
        if user.id <= 0:
            raise ValueError("User ID must be a positive integer")
        return self.user_repository.update(user)

    def delete_user(self, user_id: int) -> None:
        '''
        Удаление пользователя по ID.
        '''
        if user_id <= 0:
            raise ValueError("User ID must be a positive integer")
        self.user_repository.delete(user_id)
