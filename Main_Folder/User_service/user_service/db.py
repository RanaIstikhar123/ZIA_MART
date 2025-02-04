from sqlmodel import SQLModel, create_engine, Session
from user_service import settings

# Corrected connection string
connection_string = str(settings.DATABASE_URL).replace("postgresql", "postgresql+psycopg")
#Engine
engine = create_engine(connection_string, connect_args={}, pool_recycle=300)

# Create the database tables
def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)

# Session management
def get_session():
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()
