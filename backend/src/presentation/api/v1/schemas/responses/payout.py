from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

from src.application.dtos.payout import PayoutDTO


class PayoutResponseSchema(BaseModel):
    uuid: UUID
    game_round_uuid: UUID
    amount: int
    status: str
    telegram_payout_id: str | None
    created_at: datetime

    @classmethod
    def from_dto(cls, dto: PayoutDTO) -> "PayoutResponseSchema":
        return cls(
            uuid=dto.uuid,
            game_round_uuid=dto.game_round_uuid,
            amount=dto.amount,
            status=dto.status.value,          
            telegram_payout_id=dto.telegram_payout_id,
            created_at=dto.created_at,
        )
