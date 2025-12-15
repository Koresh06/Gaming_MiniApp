import logging
from uuid import UUID
from dataclasses import dataclass

from src.application.dtos.bet import BetDTO
from src.application.use_cases.base import UseCase, UseCaseRequest
from src.domain.entities.bet import Bet
from src.domain.exceptions.validation import DomainValidationError
from src.domain.value_object.code_games import GameCode
from src.infrastructure.database.transaction_manager.base import TransactionManager
from src.infrastructure.repositories.bet.base import BaseBetRepository


logger = logging.getLogger(__name__)


@dataclass(frozen=True, eq=False)
class CreateBetRequest(UseCaseRequest):
    user_uuid: UUID
    game_code: GameCode
    amount: int



@dataclass
class CreateBetUseCase(UseCase[CreateBetRequest, BetDTO]):
    bet_repository: BaseBetRepository
    transaction_manager: TransactionManager

    async def __call__(self, request: CreateBetRequest) -> BetDTO:
        logger.info(
            "Получен запрос на создание ставки",
            extra={
                "user_uuid": str(request.user_uuid),
                "game_code": request.game_code.value,
                "amount": request.amount,
            }
        )

        if request.amount <= 0:
            logger.warning(
                "Попытка создать ставку с некорректной суммой",
                extra={
                    "user_uuid": str(request.user_uuid),
                    "amount": request.amount,
                }
            )
            raise DomainValidationError(message="Сумма ставки должна быть положительной.")

        try:
            bet = Bet(
                user_uuid=request.user_uuid,
                game_code=request.game_code,
                amount=request.amount,
            )
        except Exception as e:
            logger.error(
                "Ошибка при создании доменной сущности Bet",
                extra={
                    "exception": str(e),
                    "request": request.__dict__,
                }
            )
            raise

        logger.info(
            "Сущность ставки успешно создана",
            extra={
                "bet_uuid": str(bet.uuid),
                "user_uuid": str(bet.user_uuid),
                "game_code": bet.game_code.value,
                "amount": bet.amount,
            }
        )

        try:
            await self.bet_repository.create(bet)
            await self.transaction_manager.commit()
        except Exception as e:
            logger.error(
                "Ошибка сохранения ставки в базе данных",
                extra={
                    "exception": str(e),
                    "bet_uuid": str(bet.uuid),
                    "user_uuid": str(bet.user_uuid),
                }
            )
            raise

        logger.info(
            "Ставка успешно сохранена в базе данных",
            extra={
                "bet_uuid": str(bet.uuid),
                "status": bet.status.value,
            }
        )

        dto = BetDTO.from_entity(bet)

        logger.info(
            "Ставка успешно создана и возвращена клиенту",
            extra={
                "bet_uuid": str(dto.uuid),
                "game_code": dto.game_code.value,
                "amount": dto.amount,
                "status": dto.status.value,
            }
        )

        return dto
