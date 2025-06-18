from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = "sqlite+aiosqlite:///./crm.db"

# Create the async engine
engine = create_async_engine(DATABASE_URL, echo=False, future=True)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# Base class for models
class Base(DeclarativeBase):
    pass

# Dependency to get a session per-request
async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close() 