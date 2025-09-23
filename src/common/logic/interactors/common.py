from src.common.types import ModelT
from src.main.infra.unit_of_work import AbstractUnitOfWork


def create_model_instance(
    *, uow: AbstractUnitOfWork, model_class: type[ModelT], validated_data: dict
) -> ModelT:
    new_entity = model_class(**validated_data)
    uow.add(new_entity)
    return new_entity

