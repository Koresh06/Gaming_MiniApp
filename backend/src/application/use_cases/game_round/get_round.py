from dataclasses import dataclass
import logging
from uuid import UUID

from src.application.dtos.game_round import GameRoundDTO
from src.application.exceptions.game_round import GameRoundNotFound
from src.application.use_cases.base import UseCase, UseCaseRequest
from src.infrastructure.repositories.game_round.base import BaseGameRoundRepository


logger = logging.getLogger(__name__)


@dataclass(frozen=True, eq=False)
class GetGameRoundRequest(UseCaseRequest):
    bet_uuid: UUID


@dataclass
class GetGameRoundUseCase(UseCase[GetGameRoundRequest, GameRoundDTO]):
    round_repository: BaseGameRoundRepository

    async def __call__(self, request: GetGameRoundRequest) -> GameRoundDTO:
        logger.info(
            "Запрос на получение игрового раунда",
            extra={"bet_uuid": str(request.bet_uuid)}
        )

        game_round = await self.round_repository.get_by_bet_uuid(request.bet_uuid)

        if game_round is None:
            logger.warning(
                "Игровой раунд не найден",
                extra={"bet_uuid": str(request.bet_uuid)}
            )
            raise GameRoundNotFound()

        logger.info(
            "Игровой раунд найден",
            extra={
                "round_uuid": str(game_round.uuid),
                "bet_uuid": str(game_round.bet_uuid),
                "user_uuid": str(game_round.user_uuid),
                "outcome_code": game_round.outcome_code.value,
                "is_win": game_round.is_win,
                "win_amount": game_round.win_amount,
            }
        )

        return GameRoundDTO.from_entity(game_round)