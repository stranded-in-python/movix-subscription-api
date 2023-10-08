from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request, status

import api.schema as schema
import core.exceptions as exc
from managers.subscription import SubcriptionManager, get_subscriptin_manager
from src.auth.users import get_current_superuser

router = APIRouter()
router.prefix = "/subscriptions"


@router.get("", summary="Get subscription", description="Get subscription by id")
async def get_subscription(
    subscription_id: UUID,
    subscriptin_manager: SubcriptionManager = Depends(get_subscriptin_manager),
) -> schema.SubscriptionRead:
    object = await subscriptin_manager.get(subscription_id)
    return schema.SubscriptionRead.model_validate(object)


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
    request: Request,
    subscription_create: schema.SubscriptionCreate,
    subscriptin_manager: SubcriptionManager = Depends(get_subscriptin_manager),
    user=Depends(get_current_superuser),
) -> schema.SubscriptionRead:
    object = await subscriptin_manager.create(
        subscription_create.model_dump(), request=request
    )
    return schema.SubscriptionRead.model_validate(object)


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
    request: Request,
    subscription_update: schema.SubscriptionUpdate,
    subscriptin_manager: SubcriptionManager = Depends(get_subscriptin_manager),
    user=Depends(get_current_superuser),
) -> schema.SubscriptionRead:
    object = await subscriptin_manager.get(subscription_update.id)

    if object is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=exc.ObjectNotExists)

    object = await subscriptin_manager.update(
        subscription_update.model_dump(), object, request=request
    )

    return schema.SubscriptionRead.model_validate(object)


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
async def delete_subscription(
    request: Request,
    subscription_id: UUID,
    subscriptin_manager: SubcriptionManager = Depends(get_subscriptin_manager),
    user=Depends(get_current_superuser),
) -> schema.SubscriptionRead:
    object = await subscriptin_manager.get(subscription_id)

    if object is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=exc.ObjectNotExists)

    object = await subscriptin_manager.delete(object, request=request)

    return schema.SubscriptionRead.model_validate(object)
