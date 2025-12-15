import logging
from uuid import UUID
from dataclasses import dataclass

from src.application.dtos.payout import PayoutDTO
from src.application.exceptions.payout import PayoutNotFound
from src.application.use_cases.base import UseCase, UseCaseRequest
from src.domain.value_object.payout_status import PayoutStatus
from src.infrastructure.database.transaction_manager.base import TransactionManager
from src.infrastructure.repositories.payout.base import BasePayoutRepository


logger = logging.getLogger(__name__)


@dataclass(frozen=True, eq=False)
class UpdatePayoutStatusRequest(UseCaseRequest):
    payout_uuid: UUID
    status: PayoutStatus
    telegram_payout_id: str | None


@dataclass
class UpdatePayoutStatusUseCase(UseCase[UpdatePayoutStatusRequest, PayoutDTO]):
    payout_repository: BasePayoutRepository
    transaction_manager: TransactionManager

    async def __call__(self, request: UpdatePayoutStatusRequest) -> PayoutDTO:
        logger.info(
            "Запрос на обновление статуса выплаты",
            extra={
                "payout_uuid": str(request.payout_uuid),
                "new_status": request.status.value,
                "telegram_payout_id": request.telegram_payout_id,
            }
        )

        payout = await self.payout_repository.get_by_uuid(request.payout_uuid)

        if payout is None:
            logger.warning(
                "Выплата не найдена, обновление невозможно",
                extra={"payout_uuid": str(request.payout_uuid)}
            )
            raise PayoutNotFound()

        logger.info(
            "Выплата найдена",
            extra={
                "payout_uuid": str(payout.uuid),
                "current_status": payout.status.value,
                "current_telegram_payout_id": payout.telegram_payout_id,
            }
        )

        payout.status = request.status
        payout.telegram_payout_id = request.telegram_payout_id

        await self.payout_repository.update(payout)
        await self.transaction_manager.commit()

        logger.info(
            "Статус выплаты успешно обновлён",
            extra={
                "payout_uuid": str(payout.uuid),
                "updated_status": payout.status.value,
                "telegram_payout_id": payout.telegram_payout_id,
            }
        )


        return PayoutDTO.from_entity(payout)
