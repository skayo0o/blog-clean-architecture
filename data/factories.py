from sqlalchemy.orm import Session
from data.repositories.user_repository import UserRepositoryImpl
from data.repositories.post_repository import PostRepositoryImpl
from data.repositories.comment_repository import CommentRepositoryImpl

class RepositoryFactory:
    @staticmethod
    def create_user_repository(db_session: Session = None):
        return UserRepositoryImpl(db_session)

    @staticmethod
    def create_post_repository(db_session: Session = None):
        return PostRepositoryImpl(db_session)

    @staticmethod
    def create_comment_repository(db_session: Session = None):
        return CommentRepositoryImpl(db_session)
