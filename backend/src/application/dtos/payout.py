from uuid import UUID
from dataclasses import dataclass
from datetime import datetime

from src.domain.entities.payout import Payout
from src.domain.value_object.payout_status import PayoutStatus


@dataclass(frozen=True, eq=False, kw_only=True)
class PayoutDTO:
    uuid: UUID
    game_round_uuid: UUID
    amount: int
    status: PayoutStatus 
    telegram_payout_id: str | None
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, payout: Payout) -> "PayoutDTO":
        return PayoutDTO(
            uuid=payout.uuid,
            game_round_uuid=payout.game_round_uuid,
            amount=payout.amount,
            status=payout.status,
            telegram_payout_id=payout.telegram_payout_id,
            created_at=payout.created_at,
            updated_at=payout.created_at,
        )