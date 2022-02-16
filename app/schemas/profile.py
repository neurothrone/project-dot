import hashlib
from datetime import datetime

from pydantic import Field

from app.data.models.profile import ProfileBase


class ProfileIn(ProfileBase):
    pass


class ProfileOut(ProfileBase):
    id: int
    last_seen_at: datetime
    avatar_hash: str | None = None

    @property
    def full_name(self) -> str:
        return f"{self.name} {self.surname}" if self.name and self.surname else ""

    def gravatar_hash(self):
        # Gravatar service requires email to be lowercase.
        # MD5 support in Python works on bytes and not on strings, therefor the
        # string must first be encoded into bytes.
        return hashlib.md5(self.account.email.lower().encode("utf-8")).hexdigest()

    def gravatar(self, size=100, default="identicon", rating="g"):
        # gravatar default size is 80x80 pixels
        url = "https://secure.gravatar.com/avatar"
        _hash = self.avatar_hash or self.gravatar_hash()
        return "{url}/{hash}?s={size}&d={default}&r={rating}".format(
            url=url, hash=_hash, size=size, default=default, rating=rating)


class ProfileUpdate(ProfileBase):
    last_seen_at: datetime = Field(default_factory=datetime.utcnow)
