from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from api.schema import ErrorCode, ErrorModel
from models.billing import PaymentStatus

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
async def update_account(account_id: UUID, payment_status: PaymentStatus):
    pass
