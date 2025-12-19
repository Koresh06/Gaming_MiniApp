from uuid import UUID
from fastapi import APIRouter, status
from dishka.integrations.fastapi import inject, FromDishka

from src.core.mediator.mediator import Mediator
from src.presentation.api.v1.schemas.requests.payout import ProcessPayoutSchema
from src.presentation.api.v1.schemas.responses.payout import PayoutResponseSchema


router = APIRouter(prefix="/payouts", tags=["Выплаты"])


# POST /payouts — инициировать выплату
@router.post(
    "/{uuid}/process",
    response_model=PayoutResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Инициализация выплаты выигрыша",
)
@inject
async def process_payout(
    uuid: UUID,
    mediator: FromDishka[Mediator],
) -> PayoutResponseSchema:
    """
    Инициирует выплату выигрыша пользователю через Telegram Stars.

    **Описание процесса:**
    - Клиент передаёт UUID игрового раунда.
    - Система находит соответствующую выплату.
    - Выполняется запрос в Telegram Stars API для отправки выигрыша пользователю.
    - Статус выплаты меняется на `pending`.

    **Request body:**
    - `game_round_uuid`: UUID раунда игры, для которого необходимо выполнить выплату.

    **Response:**
    - Объект выплаты, содержащий сумму, статус и идентификатор транзакции Stars.
    """
    request = ProcessPayoutSchema(game_round_uuid=uuid)
    dto = await mediator.handle(request.to_request())

    return PayoutResponseSchema.from_dto(dto)
