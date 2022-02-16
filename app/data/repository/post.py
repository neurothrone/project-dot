from sqlmodel import Session, select

from ..db import engine
from ..models.post import PostDB


def create(title: str, content: str) -> PostDB:
    with Session(engine) as session:
        post = PostDB(title=title, content=content)
        session.add(post)
        session.commit()
        session.refresh(post)
        return post


def get_by_title(title: str) -> PostDB | None:
    with Session(engine) as session:
        post = session.exec(select(PostDB)
                            .where(PostDB.title == title)
                            ).first()
        return post
