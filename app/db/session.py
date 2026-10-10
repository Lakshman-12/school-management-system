from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings


engine = create_async_engine(
    settings.DATABASE_URL.get_secret_value(),
    echo=settings.DEBUG,
    pool_pre_ping=True,
)


AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
        
        
        
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


# Keep your existing engine, session factory and get_db() here.


DB = Annotated[
    AsyncSession,
    Depends(get_db),
]