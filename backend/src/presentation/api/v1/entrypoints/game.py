from typing import Annotated
from fastapi import APIRouter, Body, status

from src.core.mediator import get_mediator
from src.domain.value_object.code_games import GameCode
from src.application.use_cases.game.get_all import GetGamesRequest
from src.application.use_cases.game.get_outcome_settings import GetOutcomeSettingsRequest
from src.presentation.api.v1.schemas.requests.game import UpdateOutcomeSettingsSchema
from src.presentation.api.v1.schemas.responses.game import GameOutcomeSettingResponseSchema, GameResponseSchema


router = APIRouter(prefix="/games", tags=["Игры"])


# GET /games — список игр
@router.get(
    "/",
    response_model=list[GameResponseSchema],
    status_code=status.HTTP_200_OK,
    summary="Получение списка доступных игр",
)
async def get_games() -> list[GameResponseSchema]:
    """
    Возвращает список всех игр, доступных в приложении.

    **Описание:**
    - Данные формируются на основе статического списка игр (Enum + названия).
    - Используется на главном экране Mini App.

    **Response:**
    - Список объектов, содержащих код игры и её название.
    """
    mediator = get_mediator()
    request = GetGamesRequest()

    games = await mediator.handle(request)
    return [GameResponseSchema.from_dto(g) for g in games]


# GET /games/{game_code}/settings — вероятности
@router.get(
    "/{game_code}/settings",
    response_model=list[GameOutcomeSettingResponseSchema],
    status_code=status.HTTP_200_OK,
    summary="Получение настроек вероятностей игры",
)
async def get_game_outcome_settings(
    game_code: GameCode,
) -> list[GameOutcomeSettingResponseSchema]:
    """
    Возвращает текущие настройки вероятностей исходов для указанной игры.

    **Path parameters:**
    - `game_code`: код игры (slot, dice, bowling и др.)

    **Response:**
    - Список всех исходов игры с их вероятностями, множителями и статусом активности.
    """
    mediator = get_mediator()
    request = GetOutcomeSettingsRequest(game_code=game_code)

    settings = await mediator.handle(request)
    return [GameOutcomeSettingResponseSchema.from_dto(s) for s in settings]


# POST /games/{game_code}/settings — обновление вероятностей
@router.post(
    "/{game_code}/settings",
    status_code=status.HTTP_200_OK,
    summary="Обновление вероятностей игры",
)
async def update_outcome_settings(
    game_code: GameCode,
    data: Annotated[
        UpdateOutcomeSettingsSchema,
        Body(..., description="Список настроек вероятностей"),
    ],
):
    """
    Обновляет вероятность выпадения исходов для указанной игры.

    **Описание:**
    - Используется в административной панели.
    - Перед обновлением вероятностей выполняется проверка:
      сумма всех probability должна быть равна 1.

    **Path parameters:**
    - `game_code`: код игры, для которой обновляются настройки.

    **Request body:**
    - `settings`: список исходов с probability, multiplier и is_active.

    **Response:**
    - `{ "status": "ok" }` — после успешного обновления.
    """
    mediator = get_mediator()

    request = data.to_request(game_code)
    await mediator.handle(request)

    return {"status": "ok"}
