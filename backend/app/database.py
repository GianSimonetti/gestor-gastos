from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


class Base(DeclarativeBase):
    pass


def create_database(database_url: str):
    connect_args = (
        {"check_same_thread": False}
        if database_url.startswith("sqlite")
        else {}
    )
    engine = create_engine(database_url, connect_args=connect_args)
    session_factory = sessionmaker(bind=engine, expire_on_commit=False)
    return engine, session_factory

