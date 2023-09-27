import decimal
from collections import OrderedDict
from datetime import datetime
from enum import Enum
from typing import Union
from uuid import UUID

from pydantic import BaseModel

from models.billing import Currency, PaymentStatus

# region Subscriptions


class SubscriptionBase(BaseModel):
    name: str
    is_deleted: bool

    class Config:
        orm_mode = True


class SubscriptionCreate(SubscriptionBase):
    ...


class SubscriptionRead(SubscriptionBase):
    id: UUID


class SubscriptionUpdate(SubscriptionRead):
    ...


# endregion Subscriptions


# region SubscriptionAccount


class SubscriptionAccountBase(BaseModel):
    id: UUID
    subscription_id: UUID
    status: str


class SubscriptionAccountCreate(SubscriptionAccountBase):
    user_id: UUID
    subscription_id: UUID


class SubscriptionAccountRead(BaseModel):
    id: UUID
    user_id: UUID
    subscription_id: UUID
    status: str
    expires_at: datetime


# endregion SubscriptionAccount

# region Tariff


class BaseTariff(BaseModel):
    id: UUID
    subscriptions_id: UUID


class TariffRead(BaseTariff):
    created_at: datetime
    expires_at: datetime
    duration: int
    amount: decimal.Decimal
    currency: Currency


class TariffCreate(BaseModel):
    subscriptions_id: UUID
    created_at: datetime
    expires_at: datetime
    duration: int
    amount: decimal.Decimal
    currency: Currency


class TariffUpdate(BaseModel):
    id: UUID
    subscriptions_id: UUID
    created_at: datetime
    expires_at: datetime
    duration: int
    amount: decimal.Decimal
    currency: Currency


# endregion Tariff

# region Payments


class PaymentCreate(BaseModel):
    account_id: UUID
    tarriff_id: UUID


class PaymentRead(BaseModel):
    invoice_id: UUID
    account_id: UUID
    amount: decimal.Decimal
    currency: Currency
    status: PaymentStatus
    auth: bool
    data: OrderedDict | None
    public_id: str  # Идентификатор сайта, который находится в личном кабинете


# endregion Payments

# region Errors


class ErrorModel(BaseModel):
    detail: Union[str, dict[str, str]]


class ErrorCode(str, Enum):
    ACCOUNT_NOT_EXISTS = "ACCOUNT_NOT_EXISTS"


# endregion Errors
