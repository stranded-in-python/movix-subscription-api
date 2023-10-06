import uuid
from datetime import datetime
from typing import AsyncGenerator

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, MetaData, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
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


class SAAccountStatus(SQLAlchemyBase):
    id = mapped_column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_id = mapped_column("account", ForeignKey("account.id"))
    created_at = mapped_column("created_at", DateTime)
    expires_at = mapped_column("expires_at", DateTime)
    status = mapped_column("status", String(255))

    __tablename__ = "account_status"


class AccountDB(SQLAlchemyBase):
    id = mapped_column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = mapped_column("created_at", DateTime, default=datetime.utcnow)
    modified_at = mapped_column("modified_at", DateTime, default=datetime.utcnow)
    user_id = mapped_column("user", UUID(as_uuid=True))
    subscription_id = mapped_column("subscription", ForeignKey("subscription.id"))
    tariff = mapped_column("tariff", ForeignKey("tariff.id"), nullable=True)
    expires_at = mapped_column("expires_at", DateTime, nullable=True)
    invoice_id = mapped_column("invoice", UUID(as_uuid=True), nullable=True)
    status = mapped_column("status", String(255))
    on_delete = mapped_column("on_delete", Boolean, nullable=False, default=False)

    __tablename__ = "account"


class SASubscription(SQLAlchemyBase):
    id = mapped_column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = mapped_column("name", String(255), nullable=False)
    on_delete = mapped_column("on_delete", Boolean, nullable=False, default=False)

    __tablename__ = "subscription"


class SATariff(SQLAlchemyBase):
    id = mapped_column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    subscription_id = mapped_column("subscription", ForeignKey("subscription.id"))
    created_at = mapped_column("created_at", DateTime, default=datetime.utcnow)
    expires_at = mapped_column("expires_at", DateTime, nullable=True)
    amount = mapped_column("amount", Numeric(14, 2), nullable=False)
    currency = mapped_column("currency", String(3), nullable=False)
    duration = mapped_column("duration", Integer, nullable=False)

    __tablename__ = "tariff"
