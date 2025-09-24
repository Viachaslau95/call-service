import datetime

from src.common.logic.dto import BaseDto


class RecordingDto(BaseDto):
    filename: str
    duration: int
    transcription: str | None


class CallCreateDto(BaseDto):
    caller: str
    receiver: str
    started_at: datetime.datetime


class CallResponseCreateDto(BaseDto):
    id: int


class CallDto(BaseDto):
    id: int
    caller: str
    receiver: str
    started_at: datetime.datetime
    recording: RecordingDto | None = None


class RecordingResponseDto(BaseDto):
    id: int
    filename: str