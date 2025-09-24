import typing

from fastapi import status
from fastapi.exceptions import HTTPException

from src.main.infra.sql.types import SqlAlchemyModel


class BaseHTTPException(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail: str = 'Unknown Error',
        headers: dict[str, str] | None = None,
    ) -> None:
        super().__init__(status_code=status_code, detail=detail, headers=headers)


class NotFoundException(BaseHTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_404_NOT_FOUND,
        detail: typing.Any = 'Not found.',
        headers: dict[str, str] | None = None,
        model: type[SqlAlchemyModel] | None = None,
    ) -> None:
        if model is not None:
            detail = f'{model.__name__} not found.'
        super().__init__(status_code=status_code, detail=detail, headers=headers)