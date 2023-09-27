from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

import api.schema as schema

router = APIRouter()
router.prefix = "/tariff"


@router.get(
    "/subscription/{subscription_id}",
    summary="Get tariff by subscription and date",
    description="Get tariff by subscription id and date",
)
async def get_tariff_by_subscription(
    tariff_id: UUID, date: datetime
) -> schema.TariffRead:
    pass


@router.get("/{tariff_id}", summary="Get tariff", description="Get tariff by id")
async def get_tariff(tariff_id: UUID) -> schema.TariffRead:
    pass


@router.post(
    "/",
    summary="Create tariff",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Missing token or inactive user."
        },
        status.HTTP_403_FORBIDDEN: {"description": "Not a superuser."},
    },
)
async def create_tariff(subscription: schema.TariffCreate) -> schema.TariffRead:
    pass


@router.patch(
    "/",
    summary="Update tariff",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Missing token or inactive user."
        },
        status.HTTP_403_FORBIDDEN: {"description": "Not a superuser."},
        status.HTTP_404_NOT_FOUND: {"description": "The tariff does not exist."},
    },
)
async def update_tariff(subscription: schema.TariffUpdate) -> schema.TariffRead:
    pass


@router.delete(
    "/{tariff_id}",
    summary="Delete tariff",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Missing token or inactive user."
        },
        status.HTTP_403_FORBIDDEN: {"description": "Not a superuser."},
        status.HTTP_404_NOT_FOUND: {"description": "The tariff does not exist."},
    },
)
async def delete_tariff(tariff_id: UUID) -> schema.TariffRead:
    pass
