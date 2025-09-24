from src.common.exceptions import NotFoundException
from src.common.logic.facades.common import create_model_instance
from src.main.infra.unit_of_work import AbstractUnitOfWork
from src.main.logic.dto import CallCreateDto
from src.main.logic.selectors.call import calls__find_by_id, calls__with_recording
from src.main.models import Call


async def call__create(*, uow: AbstractUnitOfWork, call_create_dto: CallCreateDto) -> Call:
    return await create_model_instance(
        uow=uow,
        model_class=Call,
        validated_data=call_create_dto.model_dump(exclude_unset=True),
    )

async def call__by_id(*, uow: AbstractUnitOfWork, call_id: int) -> Call:
    query = calls__find_by_id(call_id=call_id)
    query = calls__with_recording(query=query)
    call = await query.first_or_none(db=uow.session)
    if not call:
        raise NotFoundException(model=Call)
    return call