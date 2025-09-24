from sqlalchemy.orm import joinedload

from src.main.infra.sql.sqlalchemy import Select, select
from src.main.models import Call


def calls__all() -> Select[Call]:
    return select(Call)


def calls__find_by_id(*, query: Select[Call] | None = None, call_id: int) -> Select[Call]:
    if query is None:
        query = calls__all()
    return query.filter(Call.id == call_id)


def calls__with_recording(*, query: Select[Call] | None = None) -> Select[Call]:
    if query is None:
        query = calls__all()
    return query.options(joinedload(Call.recording))