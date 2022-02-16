from . import BaseController
from app.config import settings
from app.data.repository.user import UserRepository
from app.schemas.complex import UserOutWithProfile, UserOutWithProfileWithProjects
from app.schemas.user import UserIn, UserUpdate
from app.services import security_service
from app.shared.paginator import Paginator


class UserController(BaseController):
    repository = UserRepository
    model_out = UserOutWithProfileWithProjects
    model_name: str = "User"
    model_plural_name: str = "Users"

    @classmethod
    def create(cls, user_in: UserIn) -> UserOutWithProfileWithProjects:
        password = security_service.generate_password_hash(user_in.password)
        model_db = cls.repository.create(
            **user_in.dict(),
            hashed_password=password)
        return cls.model_out.from_orm(model_db)

    @classmethod
    def create_with_profile(cls, user_in: UserIn) -> UserOutWithProfileWithProjects:
        password = security_service.generate_password_hash(user_in.password)
        user_db = cls.repository.create_with_profile(
            **user_in.dict(),
            hashed_password=password)
        return cls.model_out.from_orm(user_db)

    @classmethod
    def get_all_ilike_username(cls, search_for: str) -> list[UserOutWithProfile]:
        users_db = cls.repository.get_all_ilike_username(search_for)
        return [UserOutWithProfile.from_orm(user) for user in users_db]

    @classmethod
    def get_all_ilike_username_paginated(cls,
                                         search_for: str,
                                         page: int,
                                         ) -> Paginator:
        users_db = cls.get_all_ilike_username(search_for)
        return Paginator(page, settings.USERS_PER_PAGE, users_db, UserOutWithProfile)

        # start = (page - 1) * USERS_PER_PAGE
        # end = start + USERS_PER_PAGE
        #
        # paginator = Paginator()
        # paginator.page = page
        #
        # users_db = cls.get_all_ilike_username(search_for)
        # paginator.total = len(users_db)
        # paginator.pages = ceil(paginator.total / USERS_PER_PAGE)
        #
        # if end < len(users_db):
        #     paginator.next_num = page + 1
        #     paginator.has_next = True
        # if page > 1:
        #     paginator.prev_num = page - 1
        #     paginator.has_prev = True
        #
        # users_db = users_db[start:start + USERS_PER_PAGE]
        # paginator.items = [UserOutWithProfile.from_orm(user) for user in users_db]
        # return paginator

    @classmethod
    def get_model_by_username(cls, username: str) -> UserOutWithProfileWithProjects | None:
        user_db = cls.get_model_by_attr(username=username)
        return cls.model_out.from_orm(user_db) if user_db else None

    @classmethod
    def get_model_by_username_with_profile(cls, username: str) -> UserOutWithProfile:
        user_db = cls.get_model_by_attr(username=username)
        return UserOutWithProfile.from_orm(user_db) if user_db else None

    @classmethod
    def get_model_by_email(cls, email: str) -> UserOutWithProfileWithProjects | None:
        user_db = cls.get_model_by_attr(email=email)
        return cls.model_out.from_orm(user_db) if user_db else None

    @classmethod
    def update_model(cls, user_id: int, user_update: UserUpdate) -> UserOutWithProfileWithProjects | None:
        model_db = super().update_model(user_id, user_update)
        return cls.model_out.from_orm(model_db)

    @classmethod
    def is_credentials_valid(cls, username: str, password: str) -> bool:
        return cls.repository.is_credentials_valid(
            username,
            password,
            security_service.is_password_valid)
