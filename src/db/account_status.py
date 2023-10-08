import typing as t
import uuid

from fastapi import Depends
from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

import models
from core.pagination import PaginateQueryParams
from db.base import SAAccountStatus, get_async_session


class SAAccountStatusDB:
    session: AsyncSession
    table: SAAccountStatus

    def __init__(self, session: AsyncSession, table: SAAccountStatus):
        self.session = session
        self.table = table
        self.model_manager = models.AccountStatus

    async def get_by_id(self, id_: uuid.UUID) -> models.AccountStatus | None:
        """Get an account status by id."""
        object_ = await self._get_object_by_id(id_)
        if not object_:
            return None
        return self.model_manager.model_validate(object_)

    async def get_by_account(
        self, id_: uuid.UUID
    ) -> t.Iterable[models.AccountStatus] | None:
        """Get an account status by subscription id."""
        objects = await self._get_objects_by_account_id(id_)
        if not objects:
            return None
        return [self.model_manager.model_validate(object_) for object_ in objects]

    async def create(self, create_dict: dict[str, t.Any]) -> models.AccountStatus:
        """Create an account status."""
        object_ = self.table(**create_dict)  # type: ignore
        self.session.add(object_)
        await self.session.commit()
        return self.model_manager.model_validate(object_)

    async def update(
        self, object_: models.AccountStatus, update_dict: dict[str, t.Any]
    ) -> models.AccountStatus:
        """Update an account status."""
        _object = self._get_object_by_id(object_.id)

        for key, value in update_dict.items():
            setattr(_object, key, value)
        self.session.add(_object)
        await self.session.commit()
        await self.session.refresh(_object)

        return self.model_manager.model_validate(_object)

    async def delete(self, id_: uuid.UUID) -> None:
        """Delete an account status."""
        statement = select(self.table).where(self.table.id == id_)
        object_ = await self._get_object(statement)
        await self.session.delete(object_)
        await self.session.commit()

    async def search(
        self, pagination_params: PaginateQueryParams, filter_param: str | None = None
    ) -> t.Iterable[models.AccountStatus]:
        """Search tariffs."""
        statement = select(self.table)
        if filter_param:
            statement.where(self.table.id == filter_param)

        statement.limit(pagination_params.page_size)
        statement.offset(
            (pagination_params.page_number - 1) * pagination_params.page_size
        )

        results = await self.session.execute(statement)

        return list(
            self.model_manager.model_validate(result[0])
            for result in results.fetchall()
        )

    async def _get_object(
        self, statement: Select[tuple[SAAccountStatus]]
    ) -> SAAccountStatus | None:
        results = await self.session.execute(statement)
        return results.unique().scalar_one_or_none()

    async def _get_objects(
        self, statement: Select[tuple[SAAccountStatus]]
    ) -> t.Iterable[SAAccountStatus] | None:
        results = await self.session.execute(statement)
        return results.unique().scalars().fetchall()

    async def _get_object_by_id(self, id_: uuid.UUID) -> SAAccountStatus | None:
        statement = select(self.table).where(self.table.id == id_)
        return await self._get_object(statement)

    async def _get_objects_by_account_id(
        self, id_: uuid.UUID
    ) -> t.Iterable[SAAccountStatus] | None:
        statement = select(self.table).where(self.table.account_id == id_)
        return await self._get_objects(statement)


async def get_account_status_db(session: AsyncSession = Depends(get_async_session)):
    yield SAAccountStatusDB(session, SAAccountStatus)  # type: ignore
