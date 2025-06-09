from sqlalchemy.orm import Session
from typing import List, Optional
from domain.models.user import User
from domain.repositories.user_repository import UserRepository
from data.models import UserORM
from data.db import SessionLocal

class UserRepositoryImpl(UserRepository):
    def __init__(self, db_session: Optional[Session] = None):
        self.db: Session = db_session or SessionLocal()

    def get_by_id(self, user_id: int) -> Optional[User]:
        user = self.db.query(UserORM).filter(UserORM.id == user_id).first()
        return self._to_domain(user) if user else None

    def get_by_username(self, username: str) -> Optional[User]:
        user = self.db.query(UserORM).filter(UserORM.username == username).first()
        return self._to_domain(user) if user else None

    def list(self) -> List[User]:
        users = self.db.query(UserORM).all()
        return [self._to_domain(u) for u in users]

    def create(self, user: User) -> User:
        user_orm = UserORM(
            username=user.username,
            email=user.email,
            registered_at=user.registered_at,
            is_active=user.is_active,
        )
        self.db.add(user_orm)
        self.db.commit()
        self.db.refresh(user_orm)
        return self._to_domain(user_orm)

    def update(self, user: User) -> User:
        user_orm = self.db.query(UserORM).filter(UserORM.id == user.id).first()
        if not user_orm:
            raise ValueError("User not found")
        user_orm.username = user.username
        user_orm.email = user.email
        user_orm.is_active = user.is_active
        self.db.commit()
        self.db.refresh(user_orm)
        return self._to_domain(user_orm)

    def delete(self, user_id: int) -> None:
        user_orm = self.db.query(UserORM).filter(UserORM.id == user_id).first()
        if user_orm:
            self.db.delete(user_orm)
            self.db.commit()

    def _to_domain(self, user_orm: UserORM) -> User:
        return User(
            id=user_orm.id,
            username=user_orm.username,
            email=user_orm.email,
            registered_at=user_orm.registered_at,
            is_active=user_orm.is_active,
        )