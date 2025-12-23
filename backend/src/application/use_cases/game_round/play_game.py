import logging
from uuid import UUID
from dataclasses import dataclass

from src.domain.entities.game_round import GameRound
from src.domain.entities.payout import Payout
from src.domain.value_object.bet_status import BetStatus
from src.application.use_cases.game_round.play_game_result import GameResult
from src.application.exceptions.bet import BetNotFound, BetNotPaid
from src.application.services.game_logic_service import GameLogicService
from src.application.use_cases.base import UseCase, UseCaseRequest
from src.application.services.game_payload_service import GamePayloadService
from src.infrastructure.database.transaction_manager.base import TransactionManager
from src.infrastructure.repositories.bet.base import BaseBetRepository
from src.infrastructure.repositories.game_outcome_settings.base import BaseGameOutcomeSettingRepository
from src.infrastructure.repositories.game_round.base import BaseGameRoundRepository
from src.infrastructure.repositories.payout.base import BasePayoutRepository


logger = logging.getLogger(__name__)


@dataclass(frozen=True, eq=False)
class PlayGameRequest(UseCaseRequest):
    bet_uuid: UUID

@dataclass
class PlayGameUseCase(UseCase[PlayGameRequest, GameResult]):
    bet_repository: BaseBetRepository
    round_repository: BaseGameRoundRepository
    outcome_repository: BaseGameOutcomeSettingRepository
    payout_repository: BasePayoutRepository
    game_logic_service: GameLogicService
    payload_service: GamePayloadService
    transaction_manager: TransactionManager

    async def __call__(self, request: PlayGameRequest) -> GameResult:
        logger.info(
            "Запуск PlayGameUseCase",
            extra={"bet_uuid": str(request.bet_uuid)}
        )

        bet = await self.bet_repository.get_by_uuid(request.bet_uuid)
        if bet is None:
            logger.warning(
                "Ставка не найдена",
                extra={"bet_uuid": str(request.bet_uuid)}
            )
            raise BetNotFound()

        logger.info(
            "Ставка загружена",
            extra={
                "bet_uuid": str(bet.uuid),
                "user_uuid": str(bet.user_uuid),
                "status": bet.status,
                "amount": bet.amount,
                "game_code": bet.game_code.value,
            },
        )

        if bet.status != BetStatus.PAID:
            logger.warning(
                "Ставка не оплачена",
                extra={
                    "bet_uuid": str(bet.uuid),
                    "status": bet.status,
                },
            )
            raise BetNotPaid()

        outcomes = await self.outcome_repository.get_active_for_game(bet.game_code)

        logger.info(
            "Загружены настройки вероятностей",
            extra={
                "bet_uuid": str(bet.uuid),
                "count": len(outcomes),
                "game_code": bet.game_code.value,
            }
        )

        self.game_logic_service.validate_probabilities(outcomes)

        logger.info(
            "Вероятности успешно провалидированы",
            extra={"game_code": bet.game_code.value}
        )

        selected = self.game_logic_service.choose_outcome(outcomes)

        logger.info(
            "Выбран исход игры",
            extra={
                "bet_uuid": str(bet.uuid),
                "outcome_code": selected.outcome_code.value,
                "probability": selected.probability,
                "multiplier": selected.multiplier,
            }
        )

        win_amount = self.game_logic_service.calculate_win_amount(bet.amount, selected)

        logger.info(
            "Вычислен выигрыш",
            extra={
                "bet_uuid": str(bet.uuid),
                "win_amount": win_amount,
                "is_win": win_amount > 0,
            }
        )

        seed = self.game_logic_service.generate_seed()

        game_round = GameRound(
            bet_uuid=bet.uuid,
            user_uuid=bet.user_uuid,
            game_code=bet.game_code,
            outcome_code=selected.outcome_code,
            is_win=win_amount > 0,
            win_amount=win_amount,
            seed=seed,
        )

        await self.round_repository.create(game_round)

        logger.info(
            "Игровой раунд создан",
            extra={
                "round_uuid": str(game_round.uuid),
                "bet_uuid": str(bet.uuid),
                "user_uuid": str(bet.user_uuid),
                "outcome_code": game_round.outcome_code.value,
                "is_win": game_round.is_win,
                "win_amount": game_round.win_amount,
                "seed": game_round.seed,
            }
        )

        if game_round.is_win:
            payout = Payout(game_round_uuid=game_round.uuid, amount=win_amount)
            await self.payout_repository.create(payout)

            logger.info(
                "Создана запись выплаты",
                extra={
                    "round_uuid": str(game_round.uuid),
                    "payout_uuid": str(payout.uuid),
                    "amount": win_amount,
                }
            )

        await self.transaction_manager.commit()

        logger.info(
            "PlayGameUseCase успешно завершён",
            extra={"round_uuid": str(game_round.uuid)}
        )

        payload = self.payload_service.build_payload(
            game_code=game_round.game_code,
            outcome_code=game_round.outcome_code,
            seed=game_round.seed,
        )

        return GameResult(
            round_uuid=game_round.uuid,
            game_code=game_round.game_code,
            outcome_code=game_round.outcome_code,
            is_win=game_round.is_win,
            win_amount=game_round.win_amount,
            payload=payload,
        )