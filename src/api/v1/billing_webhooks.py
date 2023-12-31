from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status

import models
from api.schema import ErrorCode, ErrorModel
from auth.users import get_current_superuser
from managers.account import AccountManager, get_account_manager
from managers.tariff import TariffManager, get_tariff_manager
from models import PaymentStatus

router = APIRouter()
router.prefix = "/internal/hooks/billing"


@router.post(
    "/payment",
    summary="Update account on payment",
    description="Change account status on payment operation",
    responses={
        status.HTTP_200_OK: {"description": "success"},
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Missing token or inactive user."
        },
        status.HTTP_403_FORBIDDEN: {"description": "Not a billing service user."},
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorModel,
            "content": {
                "application/json": {
                    "examples": {
                        ErrorCode.ACCOUNT_NOT_EXISTS: {
                            "summary": "A user account not exists.",
                            "value": {"detail": ErrorCode.ACCOUNT_NOT_EXISTS},
                        }
                    }
                }
            },
        },
    },
)
async def update_account(
    request: Request,
    account_id: UUID,
    tariff_id: UUID,
    payment_status: PaymentStatus,
    account_manager: AccountManager = Depends(get_account_manager),
    tariff_manager: TariffManager = Depends(get_tariff_manager),
    user=Depends(get_current_superuser),
) -> Response(status_code=status.HTTP_200_OK):
    account_status: models.SubscriptionStatus
    expires_at: datetime

    account = await account_manager.get(account_id)
    if account is None:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, detail=ErrorCode.ACCOUNT_NOT_EXISTS
        )

    tariff = await tariff_manager.get(tariff_id)
    if tariff is None:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, detail=ErrorCode.TARIFF_NOT_EXISTS
        )

    if payment_status == PaymentStatus.paid:
        account_status = models.SubscriptionStatus.active

    elif payment_status == PaymentStatus.refunded:
        account_status = models.SubscriptionStatus.inactive

    if account_status is not None:
        expires_at = account_manager.calculate_expires_at(
            account, tariff, account_status
        )
        account = await account_manager.update(
            obj_update={'status': account_status, 'expires_at': expires_at},
            object_=account,
            request=request,
        )

    return Response(status_code=status.HTTP_200_OK)
