from uuid import UUID

from pydantic import BaseModel


class Subscription(BaseModel):
    id: UUID
    name: str
