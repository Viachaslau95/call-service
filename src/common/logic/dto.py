from pydantic import BaseModel, ConfigDict


class BaseDto(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        frozen=True,
        from_attributes=True,
        populate_by_name=True,
        str_min_length=1,
    )