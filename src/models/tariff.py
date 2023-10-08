from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel

from models import Currency


class Tariff(BaseModel):
    id: UUID
    subscription_id: UUID
    created_at: datetime
    expires_at: datetime
    amount: Decimal
    currency: Currency
    duration: int  # seconds
