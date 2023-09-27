from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, Integer, MetaData, Numeric, String
from sqlalchemy.dialects.postgresql import TEXT, UUID
from sqlalchemy.orm import DeclarativeBase, mapped_column

metadata_obj = MetaData(schema="subscriptions")


class SQLAlchemyBase(DeclarativeBase):
    metadata = metadata_obj


class SubscriptionDB(SQLAlchemyBase):
    id = mapped_column("id", UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = mapped_column("currency", String(255), nullable=False)

    __tablename__ = "subscription"


class TariffDB(SQLAlchemyBase):
    id = mapped_column("id", UUID(as_uuid=True), primary_key=True, default=uuid4)
    subscription_id = mapped_column("subscription", ForeignKey("subscription.id"))
    created_at = mapped_column("created_at", DateTime)
    expires_at = mapped_column("expires_at", DateTime)
    amount = mapped_column("amount", Numeric(14, 2))
    currency = mapped_column("currency", String(3))

    __tablename__ = "tariff"


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
    status = mapped_column("currency", String(255))

    __tablename__ = "account_status"
