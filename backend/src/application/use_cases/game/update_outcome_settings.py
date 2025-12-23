import logging

from dataclasses import dataclass

from src.application.dtos.game_outcome_setting import GameOutcomeSettingInputDTO
from src.application.services.game_logic_service import GameLogicService
from src.application.use_cases.base import UseCase, UseCaseRequest
from src.domain.value_object.code_games import GameCode
from src.infrastructure.database.transaction_manager.base import TransactionManager
from src.infrastructure.repositories.game_outcome_settings.base import BaseGameOutcomeSettingRepository


logger = logging.getLogger(__name__)


@dataclass(frozen=True, eq=False)
class UpdateGameOutcomeSettingsRequest(UseCaseRequest):
    game_code: GameCode
    settings: list[GameOutcomeSettingInputDTO]


@dataclass
class UpdateGameOutcomeSettingsUseCase(UseCase[UpdateGameOutcomeSettingsRequest, None]):
    outcome_repository: BaseGameOutcomeSettingRepository
    game_logic_service: GameLogicService
    transaction_manager: TransactionManager

    async def __call__(self, request: UpdateGameOutcomeSettingsRequest) -> None:
        logger.info(
            "Запрос на обновление настроек вероятностей игры",
            extra={
                "game_code": request.game_code.value,
                "settings_count": len(request.settings),
                "outcomes": [s.outcome_code.value for s in request.settings],
            }
        )

        try:
            entities = [dto.to_entity() for dto in request.settings]
        except Exception as e:
            logger.error(
                "Ошибка преобразования DTO в сущности",
                extra={
                    "exception": str(e),
                    "game_code": request.game_code.value,
                }
            )
            raise

        logger.info(
            "Настройки преобразованы в доменные сущности",
            extra={
                "game_code": request.game_code.value,
                "entities_count": len(entities),
            }
        )

        try:
            self.game_logic_service.validate_probabilities(entities)
        except Exception as e:
            logger.error(
                "Ошибка валидации вероятностей",
                extra={
                    "exception": str(e),
                    "game_code": request.game_code.value,
                    "probabilities": [e.probability for e in entities],
                }
            )
            raise

        logger.info(
            "Вероятности успешно провалидированы",
            extra={
                "game_code": request.game_code.value,
            }
        )

        await self.outcome_repository.update_settings(request.game_code, entities)
        await self.transaction_manager.commit()

        logger.info(
            "Настройки вероятностей игры успешно обновлены",
            extra={
                "game_code": request.game_code.value,
                "updated_outcomes": [e.outcome_code.value for e in entities],
            }
        )
