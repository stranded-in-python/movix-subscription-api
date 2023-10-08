import typing as t
import uuid

from fastapi import Depends, Request

import core.exceptions as exc
from core.pagination import PaginateQueryParams
from db.subscription import SASubscriptionDB, get_subscription_db
from models import Subscription


class SubcriptionManager:
    def __init__(self, db: SASubscriptionDB) -> None:
        self.db = db

    async def create(
        self, obj_create: dict[str, t.Any], request: Request | None = None
    ) -> Subscription:
        object_ = await self.db.create(obj_create)

        await self.on_after_create(object_, request)
        return object_

    async def get(self, id_: uuid.UUID) -> Subscription | None:
        object_ = await self.db.get_by_id(id_)
        return object_

    async def update(
        self,
        obj_update: dict[str, t.Any],
        object_: Subscription,
        request: Request | None = None,
    ) -> Subscription:
        _object = await self.db.update(object_, obj_update)

        await self.on_after_update(_object, request)
        return _object

    async def delete(
        self, _object: Subscription, request: Request | None = None
    ) -> Subscription:
        await self.on_before_delete(_object, request)

        await self.db.delete(_object.id)

        await self.on_after_delete(_object, request)

        return _object

    async def get_by_name(self, name: str) -> Subscription | None:
        object_ = await self.db.get_by_name(name)

        return object_

    async def search(
        self, pagination_params: PaginateQueryParams, filter_param: str | None = None
    ) -> t.Iterable[Subscription]:
        roles = await self.db.search(pagination_params, filter_param)

        return roles

    async def on_after_create(
        self, model: Subscription, request: Request | None = None
    ) -> None:
        ...

    async def on_after_update(
        self, model: Subscription, request: Request | None = None
    ) -> None:
        ...

    async def on_before_delete(
        self, model: Subscription, request: Request | None = None
    ) -> None:
        ...

    async def on_after_delete(
        self, model: Subscription, request: Request | None = None
    ) -> None:
        ...


async def get_subscriptin_manager(db: SASubscriptionDB = Depends(get_subscription_db)):
    return SubcriptionManager(db=db)
