import typing as t
import uuid
from datetime import datetime

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
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import mapped_column

import models
from core.pagination import PaginateQueryParams
from db.base import SQLAlchemyBase, get_async_session


class SATariff(SQLAlchemyBase):
    id = mapped_column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    subscription_id = mapped_column("subscription", ForeignKey("subscription.id"))
    created_at = mapped_column("created_at", DateTime, default=datetime.utcnow)
    expires_at = mapped_column("expires_at", DateTime, nullable=True)
    amount = mapped_column("amount", Numeric(14, 2), nullable=False)
    currency = mapped_column("currency", String(3), nullable=False)
    duration = mapped_column("duration", Integer, nullable=False)

    __tablename__ = "tariff"


class SATariffDB:
    session: AsyncSession
    table: SATariff

    def __init__(self, session: AsyncSession, table: SATariff):
        self.session = session
        self.table = table
        self.model_manager = models.Tariff

    async def get_by_id(self, id_: uuid.UUID) -> models.Tariff | None:
        """Get a tariff by id."""
        object_ = await self._get_object_by_id(id_)
        if not object_:
            return None
        return self.model_manager.model_validate(object_)

    async def get_by_subscription(self, id_: uuid.UUID) -> models.Tariff | None:
        """Get a tariff by subscription id."""
        object_ = await self._get_object_by_subscription_id(id_)
        if not object_:
            return None
        return self.model_manager.model_validate(object_)

    async def create(self, create_dict: dict[str, t.Any]) -> models.Tariff:
        """Create a tariff."""
        object_ = self.table(**create_dict)  # type: ignore
        self.session.add(object_)
        await self.session.commit()
        return self.model_manager.model_validate(object_)

    async def update(
        self, object_: models.Tariff, update_dict: dict[str, t.Any]
    ) -> models.Tariff:
        """Update a tariff."""
        _object = self._get_object_by_id(object_.id)

        for key, value in update_dict.items():
            setattr(_object, key, value)
        self.session.add(_object)
        await self.session.commit()
        await self.session.refresh(_object)

        return self.model_manager.model_validate(_object)

    async def delete(self, id_: uuid.UUID) -> None:
        """Delete a tariff."""
        statement = select(self.table).where(self.table.id == id_)
        object_ = await self._get_object(statement)
        await self.session.delete(object_)
        await self.session.commit()

    async def search(
        self, pagination_params: PaginateQueryParams, filter_param: str | None = None
    ) -> t.Iterable[models.Tariff]:
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

    async def _get_object_by_id(self, id_: uuid.UUID) -> SATariff | None:
        statement = select(self.table).where(self.table.id == id_)
        return await self._get_object(statement)

    async def _get_object(self, statement: Select[tuple[SATariff]]) -> SATariff | None:
        results = await self.session.execute(statement)
        return results.unique().scalar_one_or_none()

    async def _get_object_by_subscription_id(self, id_: uuid.UUID) -> SATariff | None:
        statement = select(self.table).where(self.table.subscription_id == id_)
        return await self._get_object(statement)


async def get_tariff_db(session: AsyncSession = Depends(get_async_session)):
    yield SATariffDB(session, SATariff)  # type: ignore
