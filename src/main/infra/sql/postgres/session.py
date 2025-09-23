from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.config import config

sync_engine = create_engine(
    config.postgres.sync_uri,
    future=True,
    pool_pre_ping=True,
    pool_size=2,
    max_overflow=2,
    pool_timeout=30,
    pool_recycle=1800,
)

engine = create_async_engine(
    config.postgres.uri,
    future=True,
    pool_pre_ping=True,
    pool_size=20,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,
)

AsyncSessionBuilder = sessionmaker(  # type: ignore[call-overload]
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_async_session() -> AsyncSession:
    async with AsyncSessionBuilder() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
