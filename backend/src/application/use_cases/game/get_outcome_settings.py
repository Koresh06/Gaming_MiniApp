import logging
from dataclasses import dataclass

from src.application.dtos.game_outcome_setting import GameOutcomeSettingDTO
from src.application.use_cases.base import UseCase, UseCaseRequest
from src.domain.value_object.code_games import GameCode
from src.infrastructure.repositories.game_outcome_settings.base import BaseGameOutcomeSettingRepository


logger = logging.getLogger(__name__)


@dataclass(frozen=True, eq=False)
class GetOutcomeSettingsRequest(UseCaseRequest):
    game_code: GameCode


@dataclass
class GetOutcomeSettingsUseCase(
    UseCase[GetOutcomeSettingsRequest, list[GameOutcomeSettingDTO]]
):
    outcome_repository: BaseGameOutcomeSettingRepository

    async def __call__(self, request: GetOutcomeSettingsRequest) -> list[GameOutcomeSettingDTO]:
        logger.info(
            "Запрос на получение настроек вероятностей игры",
            extra={
                "game_code": request.game_code.value,
            }
        )

        settings = await self.outcome_repository.get_all_for_game(request.game_code)

        logger.info(
            "Настройки вероятностей игры получены",
            extra={
                "game_code": request.game_code.value,
                "settings_count": len(settings),
                "outcomes": [s.outcome_code.value for s in settings],
            }
        )

        return [GameOutcomeSettingDTO.from_entity(s) for s in settings]
