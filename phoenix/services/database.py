from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, Session

import settings


engine = create_async_engine(settings.DATABASE_URL)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def db_session():
    async with async_session() as session:
        async with session.begin():
            yield session


async def create_all():
    from phoenix.models.task import Task
    from phoenix.models.prime import Prime

    [Task, Prime]
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


__all__ = ["db_session", "Session"]
