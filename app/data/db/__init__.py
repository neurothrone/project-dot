from sqlmodel import create_engine, Session, SQLModel
from sqlmodel.sql.expression import Select, SelectOfScalar

SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore

engine = None


def init_db(db_url: str) -> None:
    global engine
    engine = create_engine(db_url, connect_args=dict(check_same_thread=False))

    import app.data.models
    SQLModel.metadata.create_all(engine)


def get_session() -> Session:
    with Session(engine) as session:
        yield session
