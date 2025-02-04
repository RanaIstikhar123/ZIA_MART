from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager

from sqlmodel import SQLModel
from payment_service import setting

# Corrected connection string for asyncpg
connection_string = str(setting.DATABASE_URL).replace("postgresql", "postgresql+asyncpg")

# Create async engine for asyncpg
async_engine = create_async_engine(connection_string, pool_recycle=300)

# Create async session factory
async_session = sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)

# Function to create database tables asynchronously
async def create_db_and_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)  # Use run_sync() to handle synchronous SQL operations

# Async context manager to provide an async session
@asynccontextmanager
async def get_session():
    async with async_session() as session:
        yield session
