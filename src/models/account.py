from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

import models


class Account(BaseModel):
    id: UUID
    created_at: datetime
    subscription_id: UUID
    user_id: UUID
    status: models.SubscriptionStatus
    invoice_id: UUID | None
    expires_at: datetime


class AccountStatus(BaseModel):
    id: UUID
    account_id: UUID
    created_at: datetime
    expires_at: datetime
    status: models.SubscriptionStatus
