from uuid import UUID

from fastapi import APIRouter, status

import api.schema as schema

router = APIRouter()
router.prefix = "/subscriptions"


@router.get(
    "/{subscription_id}",
    summary="Get subscription",
    description="Get subscription by id",
)
async def get_subscription(subscription_id: UUID):
    pass


@router.post(
    "/",
    summary="Create subscription",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Missing token or inactive user."
        },
        status.HTTP_403_FORBIDDEN: {"description": "Not a superuser."},
        status.HTTP_404_NOT_FOUND: {"description": "The subscription does not exist."},
    },
)
async def create_subscription(
    subscription: schema.SubscriptionCreate,
) -> schema.SubscriptionRead:
    pass


@router.patch(
    "/",
    summary="Update subscription",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Missing token or inactive user."
        },
        status.HTTP_403_FORBIDDEN: {"description": "Not a superuser."},
        status.HTTP_404_NOT_FOUND: {"description": "The subscription does not exist."},
    },
)
async def update_subscription(
    subscription: schema.SubscriptionUpdate,
) -> schema.SubscriptionRead:
    pass


@router.delete(
    "/{subscription_id}",
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
