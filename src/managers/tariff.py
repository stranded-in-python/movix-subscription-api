import typing as t
import uuid

from fastapi import Depends, Request

import core.exceptions as exc
from core.pagination import PaginateQueryParams
from db.tariff import SATariffDB, get_tariff_db
from models import Tariff


class TariffManager:
    def __init__(self, tariff_db: SATariffDB) -> None:
        self.tariff_db = tariff_db

    async def create(
        self, obj_create: dict[str, t.Any], request: Request | None = None
    ) -> Tariff:
        created_role = await self.tariff_db.create(obj_create)

        await self.on_after_create(created_role, request)
        return created_role

    async def get(self, tariff_id: uuid.UUID) -> Tariff | None:
        object = await self.tariff_db.get_by_id(tariff_id)

        return object

    async def update(
        self,
        obj_update: dict[str, t.Any],
        model: Tariff,
        request: Request | None = None,
    ) -> Tariff:
        updated_role = await self.tariff_db.update(model, obj_update)

        await self.on_after_update(updated_role, request)
        return updated_role

    async def delete(self, model: Tariff, request: Request | None = None) -> Tariff:
        await self.on_before_delete(model, request)

        await self.tariff_db.delete(model.id)

        await self.on_after_delete(model, request)

        return model

    async def get_by_subscription(self, sub_id: uuid.UUID) -> Tariff | None:
        model = await self.tariff_db.get_by_subscription(sub_id)

        return model

    async def search(
        self, pagination_params: PaginateQueryParams, filter_param: str | None = None
    ) -> t.Iterable[Tariff]:
        roles = await self.tariff_db.search(pagination_params, filter_param)

        return roles

    async def on_after_create(
        self, model: Tariff, request: Request | None = None
    ) -> None:
        ...

    async def on_after_update(
        self, model: Tariff, request: Request | None = None
    ) -> None:
        ...

    async def on_before_delete(
        self, model: Tariff, request: Request | None = None
    ) -> None:
        ...

    async def on_after_delete(
        self, model: Tariff, request: Request | None = None
    ) -> None:
        ...


async def get_tariff_manager(tariff_db: SATariffDB = Depends(get_tariff_db)):
    yield TariffManager(tariff_db=tariff_db)
