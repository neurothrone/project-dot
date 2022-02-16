from app.data.repository import post as post_repo


def create(title: str, content: str) -> post_repo.PostDB:
    return post_repo.create(title, content)


def get_by_title(title: str) -> post_repo.PostDB | None:
    return post_repo.get_by_title(title)
