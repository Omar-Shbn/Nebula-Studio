# db.py
from collections.abc import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from config import settings

engine = create_async_engine(
    settings.database_url,
    pool_pre_ping=True,  # test pooled connections before use (survives Postgres restarts)
)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency: one session per request, closed automatically afterwards."""
    async with async_session_maker() as session:
        yield session


async def check_database() -> None:
    """Called once at startup so a stopped or misconfigured Postgres fails loudly."""
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
    except Exception as err:
        raise RuntimeError(f"Can't connect to the database: {err}") from err
