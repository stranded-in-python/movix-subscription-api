from typing import AsyncGenerator
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, Integer, MetaData, Numeric, String
from sqlalchemy.dialects.postgresql import TEXT, UUID
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, mapped_column

from core.config import get_database_url_async

metadata_obj = MetaData(schema="subscriptions")

engine = create_async_engine(get_database_url_async())
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


class SQLAlchemyBase(DeclarativeBase):
    metadata = metadata_obj
