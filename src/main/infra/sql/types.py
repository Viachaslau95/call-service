import typing

from src.main.infra.sql.models import Base

SqlAlchemyModel = typing.TypeVar('SqlAlchemyModel', bound=Base)
