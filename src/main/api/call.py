import uuid
from pathlib import Path

import aiofiles

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from starlette import status

from src.common.exceptions import NotFoundException
from src.config import config
from src.main.infra.sql.unit_of_work import UnitOfWork
from src.main.infra.unit_of_work import AbstractUnitOfWork
from src.main.logic.dto import CallCreateDto, CallResponseCreateDto, CallDto, RecordingResponseDto
from src.main.logic.facades.call import call__create, call__by_id
from src.main.models import Recording
from src.common.celery.celery_tasks import process_recording

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


ALLOWED_EXT = {".mp3", ".wav", ".m4a", ".flac"}
MAX_FILE_SIZE = 100 * 1024 * 1024

@router.post("/{call_id}/recording/", status_code=status.HTTP_201_CREATED)
async def call_recording(
    call_id: int,
    file: UploadFile = File(...),
    uow: AbstractUnitOfWork = Depends(UnitOfWork.dependency),
) -> RecordingResponseDto:
    suffix = Path(file.filename).suffix.lower()
    if suffix not in ALLOWED_EXT:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    recording_dir = Path(config.recordings_dir) / str(call_id)
    recording_dir.mkdir(parents=True, exist_ok=True)
    file_path = recording_dir / file.filename

    written = 0
    async with aiofiles.open(file_path, "wb") as out_file:
        while True:
            chunk = await file.read(1024 * 1024)
            if not chunk:
                break
            written += len(chunk)
            if written > MAX_FILE_SIZE:
                await out_file.close()
                file_path.unlink(missing_ok=True)
                raise HTTPException(status_code=413, detail="File too large")
            await out_file.write(chunk)

    async with uow:
        try:
            await call__by_id(uow=uow, call_id=call_id)
        except NotFoundException:
            file_path.unlink(missing_ok=True)
            raise NotFoundException(status_code=404, detail="Call not found")

        relative_path = str(Path(str(call_id)) / file.filename)
        recording = Recording(
            filename=relative_path,
            duration=0,
            transcription=None,
            call_id=call_id,
        )
        uow.add(recording)
        await uow.flush()
        await uow.refresh(recording)

    process_recording.delay(recording.id, str(file_path))
    return RecordingResponseDto.model_validate(recording)
