from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

import api.schema as schema

router = APIRouter()
router.prefix = "/accounts"


@router.get(
    "/users/{user_id}",
    summary="Get user subscription accounts",
    description="Get user subscription accounts by user id",
)
async def get_user_subscription_accounts(
    user_id: UUID,
) -> list[schema.SubscriptionAccountBase]:
    pass


@router.get(
    "/{subscription_account_id}",
    summary="Get subscription account",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Missing token or inactive user."
        },
        status.HTTP_403_FORBIDDEN: {"description": "Forbidden."},
        status.HTTP_404_NOT_FOUND: {
            "description": "The subscription account does not exist."
        },
    },
)
async def create_subscription_account(
    subscription: schema.SubscriptionAccountCreate,
) -> schema.SubscriptionAccountRead:
    pass


@router.post(
    "/",
    summary="Create subscription account",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Missing token or inactive user."
        },
        status.HTTP_403_FORBIDDEN: {"description": "Not a superuser."},
        status.HTTP_404_NOT_FOUND: {
            "description": "The subscription account does not exist."
        },
    },
)
async def create_subscription_account(
    subscription: schema.SubscriptionAccountCreate,
) -> schema.SubscriptionAccountRead:
    pass


@router.patch(
    "/",
    summary="Update subscription",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Missing token or inactive user."
        },
        status.HTTP_403_FORBIDDEN: {"description": "Not a superuser."},
        status.HTTP_404_NOT_FOUND: {
            "description": "The subscription account does not exist."
        },
    },
)
async def update_subscription_account(
    subscription: schema.SubscriptionAccountRead,
) -> schema.SubscriptionAccountRead:
    pass


@router.delete(
    "/{subscription_account_id}",
    summary="Delete subscription",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Missing token or inactive user."
        },
        status.HTTP_403_FORBIDDEN: {"description": "Not a superuser."},
        status.HTTP_404_NOT_FOUND: {"description": "The subscription does not exist."},
    },
)
async def delete_subscription(subscription_id: UUID) -> schema.SubscriptionRead:
    pass
