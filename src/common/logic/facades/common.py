from src.common.logic.interactors.common import (
    create_model_instance as create_model_instance_interactor,
)
from src.common.types import ModelT

from src.main.infra.unit_of_work import AbstractUnitOfWork


async def create_model_instance(
    *, uow: AbstractUnitOfWork, model_class: type[ModelT], validated_data: dict
) -> ModelT:
    new_entity = create_model_instance_interactor(
        uow=uow, model_class=model_class, validated_data=validated_data
    )
    await uow.flush()
    await uow.refresh(new_entity)
    return new_entity
