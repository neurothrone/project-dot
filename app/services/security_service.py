from passlib.context import CryptContext

__pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated=["auto"],
    argon2__rounds=40,
)


def generate_password_hash(password: str) -> str:
    return __pwd_context.hash(password)


def is_password_valid(plain_password: str, password_hash: str) -> bool:
    return __pwd_context.verify(plain_password, password_hash)
