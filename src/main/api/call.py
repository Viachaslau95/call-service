from fastapi import APIRouter, Depends
from starlette import status

from src.main.infra.sql.unit_of_work import UnitOfWork
from src.main.infra.unit_of_work import AbstractUnitOfWork
from src.main.logic.dto import CallCreateDto, CallResponseCreateDto, CallDto
from src.main.logic.facades.call import call__create, call__by_id


router = APIRouter(prefix='/calls', tags=['Calls'])


@router.post('', status_code=status.HTTP_201_CREATED)
async def call_create(
    call_create_dto: CallCreateDto,
    uow: AbstractUnitOfWork = Depends(UnitOfWork.dependency),
) -> CallResponseCreateDto:
    call = await call__create(uow=uow, call_create_dto=call_create_dto)
    return CallResponseCreateDto.model_validate(call)


@router.get('/{call_id}', status_code=status.HTTP_200_OK)
async def get_call(
    call_id: int,
    uow: AbstractUnitOfWork = Depends(UnitOfWork.dependency),
) -> CallDto:
    call = await call__by_id(uow=uow, call_id=call_id)
    return CallDto.model_validate(call)
