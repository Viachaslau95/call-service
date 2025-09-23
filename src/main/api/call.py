from fastapi import APIRouter, Depends
from starlette import status

from src.main.infra.sql.unit_of_work import UnitOfWork
from src.main.infra.unit_of_work import AbstractUnitOfWork
from src.main.logic.dto import CallCreateDto, CallResponseCreateDto
from src.main.logic.facades.call import call__create

router = APIRouter(prefix='/calls', tags=['Calls'])


@router.post('', status_code=status.HTTP_201_CREATED)
async def call_create(
    call_create_dto: CallCreateDto,
    uow: AbstractUnitOfWork = Depends(UnitOfWork.dependency),
) -> CallResponseCreateDto:
    office = await call__create(uow=uow, call_create_dto=call_create_dto)
    return CallResponseCreateDto.model_validate(office)