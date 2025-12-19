from typing import Annotated
from fastapi import APIRouter, Body, status, Depends
from dishka.integrations.fastapi import inject, FromDishka

from src.core.mediator.mediator import Mediator
from src.domain.value_object.code_games import GameCode
from src.application.use_cases.game.get_all import GetGamesRequest
from src.application.use_cases.game.get_outcome_settings import GetOutcomeSettingsRequest
from src.presentation.api.v1.depandancies.permissions import require_admin
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
@inject
async def get_games(mediator: FromDishka[Mediator]) -> list[GameResponseSchema]:
    """
    Возвращает список всех игр, доступных в приложении.

    **Описание:**
    - Данные формируются на основе статического списка игр (Enum + названия).
    - Используется на главном экране Mini App.

    **Response:**
    - Список объектов, содержащих код игры и её название.
    """
    request = GetGamesRequest()

    games = await mediator.handle(request)
    return [GameResponseSchema.from_dto(g) for g in games]


# GET /games/{game_code}/settings — вероятности
@router.get(
    "/{game_code}/settings",
    dependencies=[Depends(require_admin)],
    response_model=list[GameOutcomeSettingResponseSchema],
    status_code=status.HTTP_200_OK,
    summary="Получение настроек вероятностей игры",
)
@inject
async def get_game_outcome_settings(
    game_code: GameCode,
    mediator: FromDishka[Mediator],
) -> list[GameOutcomeSettingResponseSchema]:
    """
    Возвращает текущие настройки вероятностей исходов для указанной игры.

    **Path parameters:**
    - `game_code`: код игры (slot, dice, bowling и др.)

    **Response:**
    - Список всех исходов игры с их вероятностями, множителями и статусом активности.
    """
    request = GetOutcomeSettingsRequest(game_code=game_code)

    settings = await mediator.handle(request)
    return [GameOutcomeSettingResponseSchema.from_dto(s) for s in settings]


# POST /games/{game_code}/settings — обновление вероятностей
@router.post(
    "/{game_code}/settings",
    dependencies=[Depends(require_admin)],
    status_code=status.HTTP_200_OK,
    summary="Обновление вероятностей игры",
)
@inject
async def update_outcome_settings(
    game_code: GameCode,
    data: Annotated[
        UpdateOutcomeSettingsSchema,
        Body(..., description="Список настроек вероятностей"),
    ],
    mediator: FromDishka[Mediator]
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
    request = data.to_request(game_code)
    await mediator.handle(request)

    return {"status": "ok"}
