from dishka.integrations.fastapi import inject, FromDishka

from src.core.mediator.mediator import Mediator


@inject
def get_mediator(
    mediator: FromDishka[Mediator],
) -> Mediator:
    return mediator
