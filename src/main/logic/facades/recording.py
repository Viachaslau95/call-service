from pathlib import Path

from src.common.exceptions import NotFoundException
from src.common.logic.facades.common import create_model_instance
from src.main.infra.unit_of_work import AbstractUnitOfWork
from src.main.logic.dto import RecordingCreateDto
from src.main.logic.facades.call import call__by_id
from src.main.models import Recording


async def recording__create(uow: AbstractUnitOfWork, call_id: int, file_path: Path) -> Recording:
    try:
        await call__by_id(uow=uow, call_id=call_id)
    except NotFoundException:
        file_path.unlink(missing_ok=True)
        raise NotFoundException(status_code=404, detail="Call not found")

    relative_path = str(Path(str(call_id)) / file_path.name)
    recording_dto = RecordingCreateDto(
        filename=relative_path,
        duration=0,
        call_id=call_id,
    )
    return await create_model_instance(
        uow=uow,
        model_class=Recording,
        validated_data=recording_dto.model_dump(exclude_unset=True)
    )
