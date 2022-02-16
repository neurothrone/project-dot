from typing import Callable

from sqlmodel import select, Session

from . import BaseRepository, engine
from ..models import ProfileDB, UserDB
from app.shared.exc import (
    EmailAlreadyTakenError,
    UserDoesNotExist,
    UsernameAlreadyTakenError)


class UserRepository(BaseRepository):
    model = UserDB

    @classmethod
    def create_with_profile(cls, **kwargs) -> UserDB:
        user = cls.model(**kwargs)
        user.profile = ProfileDB()
        user.profile.create_gravatar()

        with Session(engine) as session:
            session.add(user)
            session.commit()
            session.refresh(user)

        return user

    @classmethod
    def get_all_ilike_username(cls,
                               search_for: str
                               ) -> list[UserDB]:
        with Session(engine) as session:
            return session.exec(select(cls.model)
                                .where(cls.model.username.like(f"%{search_for}%"))
                                ).unique().all()

    @classmethod
    def get_model_by_username(cls, username: str) -> UserDB | None:
        return cls.get_model_by_attr(username=username)

    @classmethod
    def get_model_by_email(cls, email: str) -> UserDB | None:
        return cls.get_model_by_attr(email=email)

    @classmethod
    def is_credentials_valid(cls,
                             username: str,
                             password: str,
                             verify_hash_func: Callable
                             ) -> bool:
        if not verify_hash_func:
            raise NameError("Hash Function is not defined.")

        if not (user := cls.get_model_by_username(username)):
            return False

        return verify_hash_func(password, user.hashed_password)

    @classmethod
    def change_username(cls, old_username: str, new_username: str) -> UserDB | None:
        # IF the new username is the same as the user' current
        # OR already taken by another user
        if old_username == new_username or cls.get_model_by_username(new_username):
            raise UsernameAlreadyTakenError("Please try a different username.")

        if not (user := cls.get_model_by_username(old_username)):
            raise UserDoesNotExist("User not found.")

        user.username = new_username
        with Session(engine) as session:
            session.add(user)
            session.commit()
            session.refresh(user)

        return user

    @classmethod
    def change_email(cls, old_email: str, new_email: str) -> UserDB | None:
        # IF the new email is the same as the user' current
        # OR already taken by another user
        if old_email == new_email or cls.get_model_by_email(new_email):
            raise EmailAlreadyTakenError("Please try a different username.")

        if not (user := cls.get_model_by_email(old_email)):
            raise UserDoesNotExist("User not found.")

        user.email = new_email
        with Session(engine) as session:
            session.add(user)
            session.commit()
            session.refresh(user)

        return user

    @classmethod
    def change_password(cls, user_id: int, new_password: str) -> bool:
        pass
