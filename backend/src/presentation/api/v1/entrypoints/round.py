from uuid import UUID
from typing import Annotated
from fastapi import APIRouter, status, Body

from src.core.mediator import get_mediator
from src.application.use_cases.game_round.get_round import GetGameRoundRequest
from src.presentation.api.v1.schemas.requests.game_round import PlayGameSchema
from src.presentation.api.v1.schemas.responses.game_round import GameRoundResponseSchema


router = APIRouter(prefix="/rounds", tags=["Раунды"])


# POST /rounds/play — запуск игры
@router.post(
    "/play",
    response_model=GameRoundResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Запуск игры по оплаченной ставке",
)
async def play_game(
    data: Annotated[
        PlayGameSchema,
        Body(..., description="UUID ставки"),
    ],
) -> GameRoundResponseSchema:
    """
    Запускает игровой раунд на основе оплаченной ставки.

    **Описание процесса:**
    - Клиент отправляет UUID оплаченной ставки.
    - Система вычисляет исход игры согласно вероятностям.
    - Создаётся `GameRound`.
    - Если исход выигрышный, создаётся запись о выплате.

    **Request body:**
    - `uuid`: UUID ставки, которая уже оплачена Telegram Stars.

    **Response:**
    - Полная информация о раунде: исход, выигрыш, seed для анимации.
    """
    mediator = get_mediator()
    dto = await mediator.handle(data.to_request())
    return GameRoundResponseSchema.from_dto(dto)


# GET /rounds/{uuid}
@router.get(
    "/{uuid}",
    response_model=GameRoundResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Получить результат игры",
)
async def get_round(
    uuid: UUID,
) -> GameRoundResponseSchema:
    """
    Возвращает информацию о результате игрового раунда.

    **Описание:**
    - Клиент передаёт UUID ставки.
    - Если раунд уже создан — возвращается результат.
    - Используется Mini App фронтендом для отображения итогов игры.

    **Path parameters:**
    - `uuid`: UUID ставки, для которой нужно получить игровой результат.

    **Response:**
    - Данные игрового раунда: исход, выигрыш, seed, время создания.
    """
    mediator = get_mediator()
    request = GetGameRoundRequest(bet_uuid=uuid)

    dto = await mediator.handle(request)
    return GameRoundResponseSchema.from_dto(dto)
