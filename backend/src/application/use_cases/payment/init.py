from dataclasses import dataclass
from uuid import UUID

from src.application.dtos.payment import InitPaymentDTO
from src.application.exceptions.bet import BetNotFound, BetNotPaid
from src.application.services.stars_payment.base import StarsPaymentServiceBase
from src.application.use_cases.base import UseCase, UseCaseRequest
from src.domain.value_object.bet_status import BetStatus
from src.infrastructure.repositories.bet.base import BaseBetRepository
from src.infrastructure.repositories.user.base import BaseUserRepository


@dataclass(frozen=True, eq=False)
class InitPaymentRequest(UseCaseRequest):
    bet_uuid: UUID


@dataclass
class InitPaymentUseCase(UseCase[InitPaymentRequest, InitPaymentDTO]):
    bet_repository: BaseBetRepository
    user_repository: BaseUserRepository
    stars_service: StarsPaymentServiceBase

    async def __call__(self, request: InitPaymentRequest) -> InitPaymentDTO:
        bet = await self.bet_repository.get_by_uuid(request.bet_uuid)
        if bet is None:
            raise BetNotFound()

        if bet.status != BetStatus.PENDING:
            raise BetNotPaid()

        user = await self.user_repository.get_by_uuid(bet.user_uuid)

        invoice_lick: str = await self.stars_service.create_payment(
            # tg_id=user.tg_id,
            amount=bet.amount,
            bet_uuid=bet.uuid,
        )

        return InitPaymentDTO(invoice_link=invoice_lick)
