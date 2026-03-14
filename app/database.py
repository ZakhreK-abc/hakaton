from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
    AsyncEngine
)
from sqlalchemy.orm import DeclarativeBase
import os
from typing import AsyncGenerator


# DATABASE_URL = os.getenv(
#     "DATABASE_URL",
#     "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"
#     # для тестов: "sqlite+aiosqlite:///./test.db"
# )

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"

engine: AsyncEngine = create_async_engine(
    DATABASE_URL,
    echo=False,               # True = видеть все SQL-запросы в консоли
    pool_pre_ping=True,       # проверять соединение перед использованием
    pool_size=5,
    max_overflow=10,
)

async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,   # очень важно для FastAPI
    autoflush=False,
)

# Базовый класс для всех моделей
class Base(DeclarativeBase):
    pass

# Зависимость для FastAPI (yield-сессия)
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()      # коммитим только если не было исключений
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()       # всегда закрываем сессию