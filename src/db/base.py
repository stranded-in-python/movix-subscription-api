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


class SubscriptionDB(SQLAlchemyBase):
    id = mapped_column("id", UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = mapped_column("name", String(255), nullable=False)

    __tablename__ = "subscription"


class AccountDB(SQLAlchemyBase):
    id = mapped_column("id", UUID(as_uuid=True), primary_key=True, default=uuid4)
    created_at = mapped_column("created_at", DateTime)
    subscription_id = mapped_column("subscription", ForeignKey("subscription.id"))
    user_id = mapped_column("user", UUID(as_uuid=True))

    __tablename__ = "account"


class AccountStatusDB(SQLAlchemyBase):
    id = mapped_column("id", UUID(as_uuid=True), primary_key=True, default=uuid4)
    account_id = mapped_column(
        "account", ForeignKey("account.id")
    )  # uuid REFERENCES subscriptions.account(id),
    created_at = mapped_column("created_at", DateTime)
    expires_at = mapped_column("expires_at", DateTime)
    status = mapped_column("status", String(255))

    __tablename__ = "account_status"
