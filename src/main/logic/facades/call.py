from src.common.logic.facades.common import create_model_instance
from src.main.infra.unit_of_work import AbstractUnitOfWork
from src.main.logic.dto import CallCreateDto
from src.main.models import Call


async def call__create(*, uow: AbstractUnitOfWork, call_create_dto: CallCreateDto) -> Call:
    return await create_model_instance(
        uow=uow,
        model_class=Call,
        validated_data=call_create_dto.model_dump(exclude_unset=True),
    )