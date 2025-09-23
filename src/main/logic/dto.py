import datetime

from src.common.logic.dto import BaseDto


class CallCreateDto(BaseDto):
    caller: str
    receiver: str
    started_at: datetime.datetime


class CallResponseCreateDto(BaseDto):
    id: int