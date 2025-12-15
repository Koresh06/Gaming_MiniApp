import logging
from uuid import UUID
from dataclasses import dataclass

from src.application.dtos.bet import BetDTO
from src.application.exceptions.bet import BetNotFound
from src.application.use_cases.base import UseCase, UseCaseRequest
from src.domain.value_object.bet_status import BetStatus
from src.infrastructure.database.transaction_manager.base import TransactionManager
from src.infrastructure.repositories.bet.base import BaseBetRepository


logger = logging.getLogger(__name__)


@dataclass(frozen=True, eq=False)
class UpdateBetStatusRequest(UseCaseRequest):
    bet_uuid: UUID
    status: BetStatus
    telegram_transaction_id: str | None


@dataclass
class UpdateBetStatusUseCase(UseCase[UpdateBetStatusRequest, BetDTO]):
    bet_repository: BaseBetRepository
    transaction_manager: TransactionManager

    async def __call__(self, request: UpdateBetStatusRequest) -> BetDTO:

        logger.info(
            "Получен запрос на обновление статуса ставки",
            extra={
                "bet_uuid": str(request.bet_uuid),
                "new_status": request.status.value,
                "telegram_transaction_id": request.telegram_transaction_id,
            }
        )

        try:
            bet = await self.bet_repository.get_by_uuid(request.bet_uuid)
        except Exception as e:
            logger.error(
                "Ошибка при получении ставки из базы данных",
                extra={
                    "bet_uuid": str(request.bet_uuid),
                    "exception": str(e),
                }
            )
            raise

        if bet is None:
            logger.warning(
                "Ставка не найдена — обновление статуса невозможно",
                extra={
                    "bet_uuid": str(request.bet_uuid),
                }
            )
            raise BetNotFound()

        logger.info(
            "Ставка найдена, начинаем обновление",
            extra={
                "bet_uuid": str(bet.uuid),
                "old_status": bet.status.value,
            }
        )

        bet.status = request.status
        bet.telegram_transaction_id = request.telegram_transaction_id

        try:
            await self.bet_repository.update(bet)
            await self.transaction_manager.commit()
        except Exception as e:
            logger.error(
                "Ошибка при обновлении ставки в базе данных",
                extra={
                    "bet_uuid": str(bet.uuid),
                    "exception": str(e),
                }
            )
            raise

        logger.info(
            "Статус ставки успешно обновлён",
            extra={
                "bet_uuid": str(bet.uuid),
                "new_status": bet.status.value,
            }
        )

        dto = BetDTO.from_entity(bet)

        logger.debug(
            "DTO ставки перед возвращением",
            extra={
                "bet_uuid": str(dto.uuid),
                "status": dto.status.value,
            }
        )

        return dto

