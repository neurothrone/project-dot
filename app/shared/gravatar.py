import hashlib


def gravatar_hash(email: str) -> str:
    """Returns email hashed with md5.

    Gravatar service requires email to be lowercase.
    MD5 support in Python works on bytes and not on strings, therefor the
    string must first be encoded into bytes.

    Args:
        email (str): email to hash
    Returns:
        str: email hashed with md5
    """

    return hashlib.md5(email.lower().encode("utf-8")).hexdigest()
