import logging
from dataclasses import dataclass

from src.application.dtos.game import GameDTO
from src.application.use_cases.base import UseCase, UseCaseRequest
from src.domain.constants.games import GAME_DEFINITIONS


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class GetGamesRequest(UseCaseRequest):
    pass


@dataclass
class GetGamesUseCase(UseCase[GetGamesRequest, list[GameDTO]]):

    async def __call__(self, request: GetGamesRequest) -> list[GameDTO]:
        logger.info("Запрос на получение списка доступных игр")

        games = [
            GameDTO(code=code, name=name)
            for code, name in GAME_DEFINITIONS.items()
        ]

        logger.info(
            "Список игр сформирован",
            extra={
                "total_games": len(games),
                "games": [g.code.value for g in games]
            }
        )

        return games
