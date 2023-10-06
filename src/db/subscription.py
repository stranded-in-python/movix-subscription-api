import typing as t
import uuid

from fastapi import Depends
from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

import models
from core.pagination import PaginateQueryParams
from db.base import SASubscription, get_async_session


class SASubscriptionDB:
    session: AsyncSession
    table: SASubscription

    def __init__(self, session: AsyncSession, table: SASubscription):
        self.session = session
        self.table = table
        self.model_manager = models.Subscription

    async def get_by_id(self, id_: uuid.UUID) -> models.Subscription | None:
        """Get a subscription by id."""
        object_ = await self._get_object_by_id(id_)
        if not object_:
            return None
        return self.model_manager.model_validate(object_)

    async def get_by_name(self, name: str) -> models.Subscription | None:
        """Get a subscription by id."""
        object_ = await self._get_object_by_name(name)
        if not object_:
            return None
        return self.model_manager.model_validate(object_)

    async def create(self, create_dict: dict[str, t.Any]) -> models.Subscription:
        """Create a subscription."""
        object_ = self.table(**create_dict)  # type: ignore
        self.session.add(object_)
        await self.session.commit()
        return self.model_manager.model_validate(object_)

    async def update(
        self, object_: models.Subscription, update_dict: dict[str, t.Any]
    ) -> models.Subscription:
        """Update a subscription."""
        _object = self._get_object_by_id(object_.id)

        for key, value in update_dict.items():
            setattr(_object, key, value)
        self.session.add(_object)
        await self.session.commit()
        await self.session.refresh(_object)

        return self.model_manager.model_validate(_object)

    async def delete(self, id_: uuid.UUID) -> None:
        """Delete a subscription."""
        statement = select(self.table).where(self.table.id == id_)
        object_ = await self._get_object(statement)
        await self.session.delete(object_)
        await self.session.commit()

    async def search(
        self, pagination_params: PaginateQueryParams, filter_param: str | None = None
    ) -> t.Iterable[models.Subscription]:
        """Search subscriptions."""
        statement = select(self.table)
        if filter_param:
            statement.where(self.table.name == filter_param)

        statement.limit(pagination_params.page_size)
        statement.offset(
            (pagination_params.page_number - 1) * pagination_params.page_size
        )

        results = await self.session.execute(statement)

        return list(
            self.model_manager.model_validate(result[0])
            for result in results.fetchall()
        )

    async def _get_object_by_id(self, object_id: uuid.UUID) -> SASubscription | None:
        statement = select(self.table).where(self.table.id == object_id)
        return await self._get_object(statement)

    async def _get_object(
        self, statement: Select[tuple[SASubscription]]
    ) -> SASubscription | None:
        results = await self.session.execute(statement)
        return results.unique().scalar_one_or_none()

    async def _get_object_by_name(self, name: str) -> SASubscription | None:
        statement = select(self.table).where(self.table.name == name)
        return await self._get_object(statement)


async def get_subscription_db(session: AsyncSession = Depends(get_async_session)):
    yield SASubscriptionDB(session, SASubscription)  # type: ignore
