import typing as t
import uuid

from fastapi import Depends
from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    MetaData,
    Numeric,
    Select,
    String,
    select,
)
from sqlalchemy.dialects.postgresql import TEXT, UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import mapped_column

import models
from core.pagination import PaginateQueryParams
from db.base import SQLAlchemyBase, get_async_session


class AccountDB(SQLAlchemyBase):
    id = mapped_column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = mapped_column("created_at", DateTime)
    subscription_id = mapped_column("subscription", ForeignKey("subscription.id"))
    user_id = mapped_column("user", UUID(as_uuid=True))

    __tablename__ = "account"


class SAAccountDB:
    session: AsyncSession
    table: AccountDB

    def __init__(self, session: AsyncSession, table: AccountDB):
        self.session = session
        self.table = table
        self.model_manager = models.Account

    async def get_by_id(self, id_: uuid.UUID) -> models.Account | None:
        """Get an account by id."""
        object_ = await self._get_object_by_id(id_)
        if not object_:
            return None
        return self.model_manager.model_validate(object_)

    async def get_by_user_id(
        self, user_id: uuid.UUID
    ) -> t.Iterable[models.Account] | None:
        """Get an accounts by user id."""
        objects = await self._get_objects_by_user_id(user_id)
        if not objects:
            return []
        return [self.model_manager.model_validate(object_) for object_ in objects]

    async def create(self, create_dict: dict[str, t.Any]) -> models.Account:
        """Create an account."""
        object_ = self.table(**create_dict)  # type: ignore
        self.session.add(object_)
        await self.session.commit()
        return self.model_manager.model_validate(object_)

    async def update(
        self, object_: models.Account, update_dict: dict[str, t.Any]
    ) -> models.Account:
        """Update an account."""
        _object = self._get_object_by_id(object_.id)

        for key, value in update_dict.items():
            setattr(_object, key, value)
        self.session.add(_object)
        await self.session.commit()
        await self.session.refresh(_object)

        return self.model_manager.model_validate(_object)

    async def delete(self, id_: uuid.UUID) -> None:
        """Delete an account."""
        statement = select(self.table).where(self.table.id == id_)
        object_ = await self._get_object(statement)
        await self.session.delete(object_)
        await self.session.commit()

    async def search(
        self, pagination_params: PaginateQueryParams, filter_param: str | None = None
    ) -> t.Iterable[models.Account]:
        """Search accounts."""
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

    async def _get_object_by_id(self, id_: uuid.UUID) -> AccountDB | None:
        statement = select(self.table).where(self.table.id == id_)
        return await self._get_object(statement)

    async def _get_object(
        self, statement: Select[tuple[AccountDB]]
    ) -> AccountDB | None:
        results = await self.session.execute(statement)
        return results.unique().scalar_one_or_none()

    async def _get_objects(
        self, statement: Select[tuple[AccountDB]]
    ) -> t.Iterable[AccountDB] | None:
        results = await self.session.execute(statement)
        return results.unique().scalars().fetchall()

    async def _get_objects_by_user_id(
        self, id_: uuid.UUID
    ) -> t.Iterable[AccountDB] | None:
        statement = select(self.table).where(self.table.user_id == id_)
        return await self._get_objects(statement)


async def get_account_db(session: AsyncSession = Depends(get_async_session)):
    yield SAAccountDB(session, AccountDB)  # type: ignore
