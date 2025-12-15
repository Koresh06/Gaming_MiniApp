import logging
from uuid import UUID
from dataclasses import dataclass

from src.domain.entities.game_round import GameRound
from src.domain.entities.user import User
from src.domain.value_object.payout_status import PayoutStatus
from src.application.dtos.payout import PayoutDTO
from src.application.exceptions.game_round import GameRoundNotFound
from src.application.exceptions.payout import PayoutNotFound
from src.application.exceptions.user import UserNotFound
from src.application.services.stars_payment.base import StarsPaymentServiceBase
from src.application.use_cases.base import UseCase, UseCaseRequest
from src.infrastructure.repositories.game_round.base import BaseGameRoundRepository
from src.infrastructure.repositories.payout.base import BasePayoutRepository
from src.infrastructure.repositories.user.base import BaseUserRepository


logger = logging.getLogger(__name__)


@dataclass(frozen=True, eq=False)
class ProcessPayoutRequest(UseCaseRequest):
    game_round_uuid: UUID


@dataclass
class ProcessPayoutUseCase(UseCase[ProcessPayoutRequest, PayoutDTO]):
    payout_repository: BasePayoutRepository
    round_repository: BaseGameRoundRepository
    user_repository: BaseUserRepository
    stars_service: StarsPaymentServiceBase

    async def __call__(self, request: ProcessPayoutRequest) -> PayoutDTO:
        logger.info(
            "Запрос на инициализацию выплаты выигрыша",
            extra={"game_round_uuid": str(request.game_round_uuid)}
        )

        payout = await self.payout_repository.get_by_game_round_uuid(request.game_round_uuid)
        if payout is None:
            logger.warning(
                "Выплата для указанного раунда не найдена",
                extra={"game_round_uuid": str(request.game_round_uuid)}
            )
            raise PayoutNotFound()

        logger.info(
            "Запись выплаты найдена",
            extra={
                "payout_uuid": str(payout.uuid),
                "amount": payout.amount,
                "status": payout.status.value,
            }
        )

        round: GameRound | None = await self.round_repository.get_by_uuid(request.game_round_uuid)
        if round is None:
            logger.error(
                "Игровой раунд для выплаты не найден",
                extra={"game_round_uuid": str(request.game_round_uuid)}
            )
            raise GameRoundNotFound()

        logger.info(
            "Игровой раунд найден",
            extra={
                "round_uuid": str(round.uuid),
                "bet_uuid": str(round.bet_uuid),
                "user_uuid": str(round.user_uuid),
                "is_win": round.is_win,
                "win_amount": round.win_amount,
            }
        )

        user: User | None = await self.user_repository.get_by_uuid(round.user_uuid)
        if user is None:
            logger.error(
                "Пользователь для выплаты не найден",
                extra={"user_uuid": str(round.user_uuid)}
            )
            raise UserNotFound()

        logger.info(
            "Пользователь найден",
            extra={
                "user_uuid": str(user.uuid),
                "tg_id": user.tg_id,
                "stars_balance": user.stars_balance,
            }
        )

        logger.info(
            "Отправка запроса на выплату в Telegram Stars",
            extra={
                "tg_id": user.tg_id,
                "amount": payout.amount,
                "round_uuid": str(request.game_round_uuid),
            }
        )

        try:
            payout_id: str = await self.stars_service.create_payout(
                tg_id=user.tg_id,
                amount=payout.amount,
                round_uuid=request.game_round_uuid,
            )
        except Exception as e:
            logger.error(
                "Ошибка при создании выплаты в Telegram Stars",
                extra={
                    "exception": str(e),
                    "round_uuid": str(request.game_round_uuid),
                    "user_tg_id": user.tg_id,
                    "amount": payout.amount,
                }
            )
            raise

        logger.info(
            "Получен payout_id от Telegram Stars",
            extra={
                "payout_uuid": str(payout.uuid),
                "telegram_payout_id": payout_id,
            }
        )

        payout.telegram_payout_id = payout_id
        payout.status = PayoutStatus.PENDING

        await self.payout_repository.update(payout)

        logger.info(
            "Выплата обновлена и ожидает подтверждения от Stars",
            extra={
                "payout_uuid": str(payout.uuid),
                "new_status": payout.status.value,
                "telegram_payout_id": payout_id,
            }
        )

        return PayoutDTO.from_entity(payout)
