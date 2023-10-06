import types as t
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel
from sqlalchemy import UUID

from models import Currency


class InvoiceCreate(BaseModel):
    user_id: UUID
    service_id: UUID
    amount: Decimal
    currency: Currency


class InvoiceRead(BaseModel):
    id: UUID
    created_at: datetime
    modified_at: datetime
    user_id: UUID
    service_id: UUID
    status: str
    amount: float
    currency: str


class Refund(BaseModel):
    created_at: t.Optional[datetime]
    modified_at: t.Optional[datetime]
    transaction_id: t.Optional[str]
    old_transaction_id: str
    invoice_id: t.Optional[UUID]
    amount: float
    currency: t.Optional[str]
    status: t.Optional[str]
    acq_provider: t.Optional[str]
    acq_message: t.Optional[str]
    transaction_type: t.Optional[str]
