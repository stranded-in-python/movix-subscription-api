from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

import api.schema as schema

router = APIRouter()
router.prefix = "/accounts"


@router.get(
    "/{account_id}/payment",
    summary="Get subscription account payment",
    description="Get subscription account payment by id",
)
async def get_account_payment(account_id: UUID) -> schema.PaymentRead:
    pass


@router.post(
    "/{account_id}/payment",
    summary="Get subscription account payment",
    description="Get subscription account payment by id",
)
async def get_account_payment(account_id: UUID) -> schema.PaymentRead:
    pass
