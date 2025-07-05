"""
Manage database session connection
"""
import os
from typing import AsyncGenerator

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.db.session import AsyncSessionLocal


# Load env vars
load_dotenv()

DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASS = os.getenv("POSTGRES_PASSWORD")

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create async engine
engine = create_async_engine(DATABASE_URL, echo=False)

# Session factory
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)



async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency injection fo db session manager
    """
    try :
        async with AsyncSessionLocal() as session:
            yield session
    except Exception as e :
        print(e)

    finally :
        session.close()
