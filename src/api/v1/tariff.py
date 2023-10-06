from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request, status

import api.schema as schema
import core.exceptions as exc
from managers.tariff import TariffManager, get_tariff_manager
from src.auth.users import get_current_superuser

router = APIRouter()
router.prefix = "/tariffs"


@router.get(
    "/subscription",
    summary="Get tariff by subscription and date",
    description="Get tariff by subscription id and date",
)
async def get_tariff_by_subscription(
    subscription_id: UUID,
    date: datetime,
    tariff_manager: TariffManager = Depends(get_tariff_manager),
) -> schema.TariffRead:
    object = await tariff_manager.get_by_subscription(subscription_id)
    return schema.TariffRead.model_validate(object)


@router.get("", summary="Get tariff", description="Get tariff by id")
async def get_tariff(
    tariff_id: UUID,
    tariff_manager: TariffManager = Depends(get_tariff_manager),
    user=Depends(get_current_superuser),
) -> schema.TariffRead:
    object = await tariff_manager.get(tariff_id)
    if object is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=exc.ObjectNotExists)
    return schema.TariffRead.model_validate(object)


@router.post(
    "",
    summary="Create tariff",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Missing token or inactive user."
        },
        status.HTTP_403_FORBIDDEN: {"description": "Not a superuser."},
    },
)
async def create_tariff(
    request: Request,
    tariff_create: schema.TariffCreate,
    tariff_manager: TariffManager = Depends(get_tariff_manager),
    user=Depends(get_current_superuser),
) -> schema.TariffRead:
    object = await tariff_manager.create(tariff_create.model_dump(), request=request)
    return schema.TariffRead.model_validate(object)


@router.put(
    "",
    summary="Update tariff",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Missing token or inactive user."
        },
        status.HTTP_403_FORBIDDEN: {"description": "Not a superuser."},
        status.HTTP_404_NOT_FOUND: {"description": "The tariff does not exist."},
    },
)
async def update_tariff(
    request: Request,
    tariff_update: schema.TariffUpdate,
    tariff_manager: TariffManager = Depends(get_tariff_manager),
    user=Depends(get_current_superuser),
) -> schema.TariffRead:
    object = await tariff_manager.get(tariff_update.id)

    if object is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=exc.ObjectNotExists)

    object = await tariff_manager.update(
        tariff_update.model_dump(), object, request=request
    )

    return schema.TariffRead.model_validate(object)


@router.delete(
    "",
    summary="Delete tariff",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Missing token or inactive user."
        },
        status.HTTP_403_FORBIDDEN: {"description": "Not a superuser."},
        status.HTTP_404_NOT_FOUND: {"description": "The tariff does not exist."},
    },
)
async def delete_tariff(
    request: Request,
    tariff_id: UUID,
    tariff_manager: TariffManager = Depends(get_tariff_manager),
    user=Depends(get_current_superuser),
) -> schema.TariffRead:
    object = await tariff_manager.get(tariff_id)

    if object is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=exc.ObjectNotExists)

    object = await tariff_manager.delete(object, request=request)

    return schema.TariffRead.model_validate(object)
