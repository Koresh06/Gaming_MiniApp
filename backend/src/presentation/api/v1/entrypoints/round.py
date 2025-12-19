from uuid import UUID
from typing import Annotated
from fastapi import APIRouter, status, Body
from dishka.integrations.fastapi import inject, FromDishka


from src.core.mediator.mediator import Mediator
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
@inject
async def play_game(
    data: Annotated[
        PlayGameSchema,
        Body(..., description="UUID ставки"),
    ],
    mediator: FromDishka[Mediator],
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
    dto = await mediator.handle(data.to_request())
    return GameRoundResponseSchema.from_dto(dto)


# GET /rounds/{uuid}
@router.get(
    "/{uuid}",
    response_model=GameRoundResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Получить результат игры",
)
@inject
async def get_round(
    uuid: UUID,
    mediator: FromDishka[Mediator],
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
    request = GetGameRoundRequest(round_uuid=uuid)

    dto = await mediator.handle(request)
    return GameRoundResponseSchema.from_dto(dto)
