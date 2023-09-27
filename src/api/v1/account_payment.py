from uuid import UUID

from fastapi import APIRouter

import api.schema as schema

router = APIRouter()
router.prefix = "/accounts"


@router.get(
    "/{account_id}/invoice",
    summary="Get subscription account invoice",
    description="Get subscription account invoice by id",
)
async def get_account_invoice(account_id: UUID) -> schema.InvoiceRead:
    pass


@router.post(
    "/invoice",
    summary="Create invoice subscription account",
    description="Create subscription account invoice by id",
)
async def create_invoice(invoice: schema.InvoiceCreate) -> schema.InvoiceRead:
    pass


@router.post(
    "/{account_id}/refund/{invoice_id}",
    summary="Create refund account payment",
    description="Create subscription account payment by id",
)
async def create_refund(account_id: UUID, invoice_id: UUID) -> schema.InvoiceRead:
    pass
