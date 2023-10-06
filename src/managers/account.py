import typing as t
import uuid
from datetime import datetime, timedelta

from fastapi import Depends, Request

import core.exceptions as exc
from core.pagination import PaginateQueryParams
from db.account import SAAccountDB, get_account_db
from db.account_status import SAAccountStatusDB, get_account_status_db
from models import Account, AccountStatus, SubscriptionStatus, Tariff


class AccountManager:
    def __init__(
        self, account_db: SAAccountDB, account_status_db: SAAccountStatusDB
    ) -> None:
        self.account_db = account_db
        self.account_status_db = account_status_db

    async def create(
        self, obj_create: dict[str, t.Any], request: Request | None = None
    ) -> Account:
        object_ = await self.account_db.create(obj_create)

        await self.on_after_create(object_, request)
        return object_

    async def get(self, obj_id: uuid.UUID) -> Account | None:
        object = await self.account_db.get_by_id(obj_id)

        return object

    async def update(
        self,
        obj_update: dict[str, t.Any],
        object_: Account,
        request: Request | None = None,
    ) -> Account:
        _object = await self.account_db.update(object_, obj_update)

        await self.on_after_update(_object, request)
        return _object

    async def delete(self, object_: Account, request: Request | None = None) -> Account:
        await self.on_before_delete(object_, request)

        await self.account_db.delete(object_.id)

        await self.on_after_delete(object_, request)

        return object_

    async def get_by_user_id(self, user_id: uuid.UUID) -> t.Iterable[Account]:
        objects = await self.account_db.get_by_user_id(user_id)

        return objects

    async def search(
        self, pagination_params: PaginateQueryParams, filter_param: str | None = None
    ) -> t.Iterable[Account]:
        roles = await self.account_db.search(pagination_params, filter_param)

        return roles

    async def on_after_create(
        self, object_: Account, request: Request | None = None
    ) -> None:
        create_dict = {"account_id": object_.id, "status": object_.status.value}
        await self.account_status_db.create(create_dict)

    async def on_after_update(
        self, object_: Account, request: Request | None = None
    ) -> None:
        create_dict = {"account_id": object_.id, "status": object_.status.value}
        await self.account_status_db.create(create_dict)

    async def on_before_delete(
        self, object_: Account, request: Request | None = None
    ) -> None:
        ...

    async def on_after_delete(
        self, object_: Account, request: Request | None = None
    ) -> None:
        ...

    async def calculate_expires_at(
        self, object_: Account, tariff: Tariff, status: SubscriptionStatus
    ) -> datetime:
        expires_at: datetime

        if status == SubscriptionStatus.active:
            expires_at = object_.expires_at + timedelta(seconds=tariff.duration)
        else:
            expires_at = datetime.now() + timedelta(seconds=tariff.duration)

        return expires_at


async def get_account_manager(
    account_db: SAAccountDB = Depends(get_account_db),
    account_status_db: SAAccountStatusDB = Depends(get_account_status_db),
):
    yield AccountManager(account_db=account_db, account_status_db=account_status_db)
