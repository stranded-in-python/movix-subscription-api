from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status

import api.schema as schema
import models as models
from auth.users import get_current_user
from managers.account import AccountManager, get_account_manager
from managers.billing import BillingManager, get_billing_manager
from managers.tariff import TariffManager, get_tariff_manager

router = APIRouter()
router.prefix = "/accounts"


@router.get(
    "/{account_id}/invoice",
    summary="Get subscription account invoice",
    description="Get subscription account invoice by id",
)
async def get_account_invoice(
    request: Request,
    account_id: UUID,
    account_manager: AccountManager = Depends(get_account_manager),
    billing_manager: BillingManager = Depends(get_billing_manager),
    user=Depends(get_current_user),
) -> schema.InvoiceRead:
    account = await account_manager.get(account_id)
    if account is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="account not found")
    if account.user_id != user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN)

    invoice = await billing_manager.get_ivoice_by_account(account.id)

    return invoice


@router.post(
    "/invoice",
    summary="Create invoice subscription account",
    description="Create subscription account invoice by id",
)
async def create_invoice(
    request: Request,
    invoice_create: schema.InvoiceCreate,
    account_manager: AccountManager = Depends(get_account_manager),
    tariff_manager: TariffManager = Depends(get_tariff_manager),
    billing_manager: BillingManager = Depends(get_billing_manager),
    user=Depends(get_current_user),
) -> schema.InvoiceRead:
    account = await account_manager.get(invoice_create.account_id)
    if account is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="account not found")
    if account.user_id != user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN)

    tariff = await tariff_manager.get(invoice_create.tariff_id)
    if tariff is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="tariff not found")
    if tariff.subscription_id != account.subscription_id:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="the tariff does not match the account subscription",
        )

    invoice_create = models.InvoiceCreate(
        user_id=account.id,
        service_id=account.tariff_id,
        amount=tariff.amount,
        currency=tariff.currency,
    )
    invoice = await billing_manager.create_invoice(invoice_create)

    return invoice


@router.post(
    "/{account_id}/refund",
    summary="Create refund account payment",
    description="Create subscription account payment by id",
)
async def create_refund(
    account_id: UUID,
    account_manager: AccountManager = Depends(get_account_manager),
    billing_manager: BillingManager = Depends(get_billing_manager),
    user=Depends(get_current_user),
) -> Response(status_code=status.HTTP_202_ACCEPTED):
    account = await account_manager.get(account_id)
    if account is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="account not found")
    if account.user_id != user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN)
    if account.status != models.SubscriptionStatus.active:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="account not active")

    if account.invoice_id is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="no invoice")

    await billing_manager.create_refund(account.invoice_id)

    return Response(status_code=status.HTTP_202_ACCEPTED)
