from app.shared.access import AccessLevel


class AuthMixin:
    @property
    def is_authenticated(self) -> bool:
        return False

    @property
    def is_active(self) -> bool:
        return False

    @property
    def is_anonymous(self) -> bool:
        return True

    @classmethod
    def get_id(cls):
        return None

    @property
    def is_admin(self) -> bool:
        return False

    @property
    def access_level(self) -> AccessLevel:
        return AccessLevel.GUEST


class AnonymousUser(AuthMixin):
    pass
