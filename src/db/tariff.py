import typing as t
import uuid
from uuid import uuid4

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
from sqlalchemy.orm import DeclarativeBase, mapped_column

import models.tariff as models
from core.pagination import PaginateQueryParams
from db.base import SQLAlchemyBase, get_async_session


class SATariff(SQLAlchemyBase):
    id = mapped_column("id", UUID(as_uuid=True), primary_key=True, default=uuid4)
    subscription_id = mapped_column("subscription", ForeignKey("subscription.id"))
    created_at = mapped_column("created_at", DateTime)
    expires_at = mapped_column("expires_at", DateTime)
    amount = mapped_column("amount", Numeric(14, 2))
    currency = mapped_column("currency", String(3))

    __tablename__ = "tariff"


class SATariffDB:
    session: AsyncSession
    user_table: SATariff

    def __init__(self, session: AsyncSession, table: SATariff):
        self.session = session
        self.table = table
        self.model_manager = models.Tariff

    async def get_by_id(self, model_id: uuid.UUID) -> models.Tariff | None:
        """Get a tariff by id."""
        model = await self._get_model_by_id(model_id)
        if not model:
            return None
        return self.model_manager.model_validate(model)

    async def get_by_subscription(self, sub_id: uuid.UUID) -> models.Tariff | None:
        """Get a tariff by id."""
        model = await self._get_model_by_subscription_id(sub_id)
        if not model:
            return None
        return self.model_manager.model_validate(model)

    async def create(self, create_dict: dict[str, t.Any]) -> models.Tariff:
        """Create a tariff."""
        model = self.table(**create_dict)  # type: ignore
        self.session.add(model)
        await self.session.commit()
        return self.model_manager.model_validate(model)

    async def update(
        self, model: models.Tariff, update_dict: dict[str, t.Any]
    ) -> models.Tariff:
        """Update a tariff."""
        _model = self._get_model_by_id(model.id)

        for key, value in update_dict.items():
            setattr(_model, key, value)
        self.session.add(_model)
        await self.session.commit()
        await self.session.refresh(_model)

        return self.model_manager.model_validate(_model)

    async def delete(self, tariff_id: uuid.UUID) -> None:
        """Delete a tariff."""
        statement = select(self.table).where(self.table.id == tariff_id)
        role_to_delete = await self._get_model(statement)
        await self.session.delete(role_to_delete)
        await self.session.commit()

    async def search(
        self, pagination_params: PaginateQueryParams, filter_param: str | None = None
    ) -> t.Iterable[models.Tariff]:
        """Search a tariffs."""
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

    async def _get_model_by_id(self, model_id: uuid.UUID) -> SATariff | None:
        statement = select(self.table).where(self.table.id == model_id)
        return await self._get_model(statement)

    async def _get_model_by_subscription_id(self, sub_id: uuid.UUID) -> SATariff | None:
        statement = select(self.table).where(self.table.subscription_id == sub_id)
        return await self._get_model(statement)

    async def _get_model(self, statement: Select[tuple[SATariff]]) -> SATariff | None:
        results = await self.session.execute(statement)
        return results.unique().scalar_one_or_none()


async def get_tariff_db(session: AsyncSession = Depends(get_async_session)):
    yield SATariffDB(session, SATariff)  # type: ignore
