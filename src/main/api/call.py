from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from starlette import status

from src.common.celery.celery_tasks import process_recording
from src.main.infra.sql.unit_of_work import UnitOfWork
from src.main.infra.unit_of_work import AbstractUnitOfWork
from src.main.logic.dto import CallCreateDto, CallDto, CallResponseCreateDto, RecordingResponseDto
from src.main.logic.facades.call import call__by_id, call__create
from src.main.logic.facades.recording import recording__create
from src.main.logic.interactors.recording import save_uploaded_file, validate_extension

router = APIRouter(prefix='/calls', tags=['Calls'])


@router.post('', status_code=status.HTTP_201_CREATED)
async def call_create(
    call_create_dto: CallCreateDto, uow: AbstractUnitOfWork = Depends(UnitOfWork.dependency)
) -> CallResponseCreateDto:
    call = await call__create(uow=uow, call_create_dto=call_create_dto)
    return CallResponseCreateDto.model_validate(call)


@router.get('/{call_id}', status_code=status.HTTP_200_OK)
async def get_call(
    call_id: int, uow: AbstractUnitOfWork = Depends(UnitOfWork.dependency)
) -> CallDto:
    call = await call__by_id(uow=uow, call_id=call_id)
    return CallDto.model_validate(call)


ALLOWED_EXT = {'.mp3', '.wav', '.m4a', '.flac'}
MAX_FILE_SIZE = 100 * 1024 * 1024


@router.post('/{call_id}/recording/', status_code=status.HTTP_201_CREATED)
async def call_recording(
    call_id: int,
    file: UploadFile = File(...),
    uow: AbstractUnitOfWork = Depends(UnitOfWork.dependency),
) -> RecordingResponseDto:
    if not file.filename:
        raise HTTPException(status_code=400, detail='Filename is missing')
    validate_extension(file.filename)
    file_path = await save_uploaded_file(call_id=call_id, file=file)

    recording = await recording__create(uow=uow, call_id=call_id, file_path=file_path)

    process_recording.delay(recording.id, str(file_path))
    return RecordingResponseDto.model_validate(recording)
