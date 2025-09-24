import typing

from sqlalchemy import BinaryExpression, Result
from sqlalchemy import Select as SqlalchemySelect
from sqlalchemy.engine import Row
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute

from src.main.infra.sql.types import SqlAlchemyModel


class Select(SqlalchemySelect[SqlAlchemyModel]):  # type: ignore[type-var]
    inherit_cache = True

    async def execute(self, db: AsyncSession) -> list[SqlAlchemyModel]:
        query = self
        result = await db.execute(query)
        fields_to_prefetch = self._fields_to_prefetch(result)
        rows = result.unique().all()
        return [
            self._instance_with_prefetched_fields(fields=fields_to_prefetch, row=row)
            for row in rows
        ]

    async def first_or_none(self, db: AsyncSession) -> SqlAlchemyModel | None:
        query = self
        result = await db.execute(query)
        fields_to_prefetch = self._fields_to_prefetch(result)
        row = result.unique().first()
        if row is None:
            return None
        return self._instance_with_prefetched_fields(fields=fields_to_prefetch, row=row)

    @staticmethod
    def _fields_to_prefetch(result: Result) -> list[str]:
        return list(result.keys())[1:]

    @staticmethod
    def _instance_with_prefetched_fields(fields: list[str], row: Row) -> SqlAlchemyModel:
        instance = row[0]
        for field, value in zip(fields, row[1:], strict=False):
            setattr(instance, field, value)
        return instance


def select(entity: type[SqlAlchemyModel]) -> Select[SqlAlchemyModel]:
    return Select(entity)


def instance_or_id_filter(
    field: InstrumentedAttribute, instance: SqlAlchemyModel | int
) -> BinaryExpression:
    return typing.cast(
        BinaryExpression, field == (instance if isinstance(instance, int) else instance.id)
    )
