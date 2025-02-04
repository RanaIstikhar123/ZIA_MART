from sqlmodel import SQLModel, Field, create_engine, Session, select
from product_service import setting
from contextlib import contextmanager


import asyncio
# Corrected connection string
connection_string = str(setting.DATABASE_URL).replace("postgresql", "postgresql+psycopg")
#Engine
engine = create_engine(connection_string, connect_args={}, pool_recycle=300)


# Corrected metadata reference
def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


# Fixed typing and async function signature


# @contextmanager
def get_session():
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()