"""
Manage database session connection
"""
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from app.config.settings import settings_config


# Create async engine
engine = create_async_engine(settings_config.DB_URL, echo=False)

# Session factory
AsyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def init_db():
    """
    sync tables
    """
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
   Generator for database table sync Dependency injection fo db session manager
    """
    try :
        async with AsyncSessionLocal() as session:
            yield session
    except Exception as e :
        raise

    finally :
        session.close()
