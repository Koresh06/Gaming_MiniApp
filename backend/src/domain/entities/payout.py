from dataclasses import dataclass
from uuid import UUID

from src.domain.entities.base import Entity
from src.domain.exceptions.validation import DomainValidationError
from src.domain.value_object.payout_status import PayoutStatus


@dataclass(kw_only=True)
class Payout(Entity):
    game_round_uuid: UUID
    amount: int
    status: PayoutStatus = PayoutStatus.PENDING
    telegram_payout_id: str | None = None

    def __post_init__(self):
        if self.amount <= 0:
            raise DomainValidationError(message="Сумма выплаты должна быть > 0.")