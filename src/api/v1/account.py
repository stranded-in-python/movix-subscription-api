from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request, status

import api.schema as schema
import core.exceptions as exc
from managers.account import AccountManager, get_account_manager
from src.auth.users import get_current_superuser, get_current_user

router = APIRouter()
router.prefix = "/accounts"


@router.get(
    "/users/me",
    summary="Get user subscription accounts",
    description="Get user subscription accounts by user id",
)
async def get_me_subscription_accounts(
    account_manager: AccountManager = Depends(get_account_manager),
    user=Depends(get_current_user),
) -> list[schema.SubscriptionAccountBase]:
    objects = await account_manager.get_by_user_id(user.id)

    return [schema.SubscriptionAccountBase.model_validate(object) for object in objects]


@router.get(
    "/users",
    summary="Get user subscription accounts",
    description="Get user subscription accounts by user id",
)
async def get_user_subscription_accounts(
    user_id: UUID,
    account_manager: AccountManager = Depends(get_account_manager),
    user=Depends(get_current_superuser),
) -> list[schema.SubscriptionAccountBase]:
    objects = await account_manager.get_by_user_id(user_id)

    return [schema.SubscriptionAccountBase.model_validate(object) for object in objects]


@router.get(
    "",
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
async def get_subscription_account(
    subscription_account_id: UUID,
    account_manager: AccountManager = Depends(get_account_manager),
    user=Depends(get_current_superuser),
) -> schema.SubscriptionAccountRead:
    object = await account_manager.get(subscription_account_id)

    if object is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=exc.ObjectNotExists)

    return schema.SubscriptionAccountRead.model_validate(object)


@router.post(
    "",
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
    rerequest: Request,
    subscription: schema.SubscriptionAccountCreate,
    account_manager: AccountManager = Depends(get_account_manager),
    user=Depends(get_current_superuser),
) -> schema.SubscriptionAccountRead:
    object = await account_manager.create(subscription.model_dump(), request=rerequest)

    return schema.SubscriptionAccountRead.model_validate(object)


@router.patch(
    "",
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
    rerequest: Request,
    subscription: schema.SubscriptionAccountRead,
    account_manager: AccountManager = Depends(get_account_manager),
    user=Depends(get_current_superuser),
) -> schema.SubscriptionAccountRead:
    object = await account_manager.get(subscription.id)

    if object is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=exc.ObjectNotExists)

    try:
        object = await account_manager.update(
            subscription.model_dump(), object, request=rerequest
        )
    except exc.ObjectNotExists:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=exc.ObjectNotExists)

    return schema.SubscriptionAccountRead.model_validate(object)


@router.delete(
    "",
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
    rerequest: Request,
    subscription_id: UUID,
    account_manager: AccountManager = Depends(get_account_manager),
    user=Depends(get_current_superuser),
) -> schema.SubscriptionAccountRead:
    object = await account_manager.get(subscription_id)
    if object is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=exc.ObjectNotExists)
    object = await account_manager.delete(object)

    return schema.SubscriptionAccountRead.model_validate(object)
