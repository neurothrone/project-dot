from enum import IntEnum
from functools import wraps
from typing import Callable

from flask import flash, redirect, url_for
from flask_login import current_user


class AccessLevel(IntEnum):
    GUEST = 0
    USER = 1
    ADMIN = 2

    def __str__(self) -> str:
        return AccessLevel(self.value).name

    @classmethod
    def create(cls, name: str) -> "AccessLevel":
        match name:
            case AccessLevel.GUEST.name:
                return cls(0)
            case AccessLevel.USER.name:
                return cls(1)
            case AccessLevel.ADMIN.name:
                return cls(2)

    @staticmethod
    def has_access(level: "AccessLevel", required: "AccessLevel") -> bool:
        return level >= required


# NOTE: redundant now that access_level_required() decorator works properly
def admin_required(func: Callable):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not hasattr(current_user, "is_admin") or not current_user.is_admin:
            flash("This page is only accessible to an admin.", category="warning")
            return redirect(url_for("open.index"))
        return func(*args, **kwargs)

    return decorated_view


def access_level_required(level: AccessLevel):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not current_user.has_access(level):
                flash("This page is not accessible to you.", category="warning")
                return redirect(url_for("open.index"))
            return func(*args, **kwargs)

        return wrapper

    return decorator
