# db.py
from sqlmodel import SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from contextlib import asynccontextmanager
from inventory_service import setting

# Corrected connection string for async engine
connection_string = str(setting.DATABASE_URL).replace("postgresql", "postgresql+psycopg")

# Async engine for asynchronous sessions
async_engine = create_async_engine(connection_string, pool_recycle=300)

# Function to create the database tables
async def create_db_and_tables() -> None:
    async with async_engine.begin() as  conn:
        await conn.run_sync(SQLModel.metadata.create_all)

# Async session for database operations
@asynccontextmanager
async def get_session():
    async with AsyncSession(async_engine) as session:  # Use "async with"
        try:
            yield session
        finally:
            await session.close() 
