from sqlmodel import create_engine, Session, SQLModel
from sqlmodel.sql.expression import Select, SelectOfScalar

from app.config import ConfigType, settings

SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore

engine = None


def init_db(config_type: ConfigType) -> None:
    global engine
    engine = create_engine(settings.get_db_url(config_type),
                           connect_args=dict(check_same_thread=False))

    import app.data.models
    SQLModel.metadata.create_all(engine)


def get_session() -> Session:
    with Session(engine) as session:
        yield session
