from uuid import UUID
from typing import Annotated
from fastapi import APIRouter, status, Body

from src.core.mediator import get_mediator
from src.application.use_cases.bet.get_by_uuid import GetBetByUUIDRequest
from src.presentation.api.v1.schemas.requests.bet import CreateBetSchema, InitPaymentSchema
from src.presentation.api.v1.schemas.responses.bet import BetResponseSchema, InitPaymentResponseSchema


router = APIRouter(prefix="/bets", tags=["Ставки"])


# POST /bets — создание ставки
@router.post(
    "/",
    response_model=BetResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Создание ставки",
)
async def create_bet(
    data: Annotated[
        CreateBetSchema,
        Body(..., description="Данные для создания ставки"),
    ],
) -> BetResponseSchema:
    """
    Создаёт новую ставку для выбранной игры и пользователя.

    **Описание процесса:**
    - Пользователь указывает сумму ставки и игру.
    - Система создаёт Bet со статусом `pending`.
    - Далее Mini App формирует Telegram Stars Invoice (не в этом эндпоинте).
    - После оплаты через Stars происходит выполнение раунда.

    **Request body:**
    - `user_uuid`: UUID пользователя  
    - `game_code`: код игры  
    - `amount`: сумма ставки в Stars  

    **Response:**
    - Объект ставки со статусом `pending` и UUID.
    """
    mediator = get_mediator()
    dto = await mediator.handle(data.to_request())
    return BetResponseSchema.from_dto(dto)

# POST /bets/{uuid}/init
@router.post(
    "/{uuid}/init",
    summary="Создать Stars оплату ставки",
    response_model=InitPaymentResponseSchema,
)
async def init_payment(uuid: UUID):
    mediator = get_mediator()

    request = InitPaymentSchema(bet_uuid=uuid)
    dto = await mediator.handle(request.to_request())

    return InitPaymentResponseSchema.from_dto(dto)



# GET /bets/{uuid}
@router.get(
    "/{uuid}",
    response_model=BetResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Получение статуса ставки",
)
async def get_bet(
    uuid: UUID,
) -> BetResponseSchema:
    """
    Возвращает информацию о ставке по её UUID.

    **Описание:**
    - Используется Mini App для проверки статуса оплаты ставки.
    - Ставка может находиться в статусах: `pending`, `paid`, `failed`.

    **Path parameters:**
    - `uuid`: UUID созданной ставки  

    **Response:**
    - Объект `BetResponseSchema` с полным состоянием ставки.
    """
    mediator = get_mediator()
    request = GetBetByUUIDRequest(bet_uuid=uuid)

    dto = await mediator.handle(request)
    return BetResponseSchema.from_dto(dto)
