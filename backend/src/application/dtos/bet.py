from uuid import UUID
from dataclasses import dataclass
from datetime import datetime

from src.domain.entities.bet import Bet
from src.domain.value_object.bet_status import BetStatus
from src.domain.value_object.code_games import GameCode


@dataclass(frozen=True, eq=False, kw_only=True)
class BetDTO:
    uuid: UUID
    user_uuid: UUID
    game_code: GameCode
    amount: int
    status: BetStatus
    telegram_transaction_id: str | None
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, bet: Bet) -> "BetDTO":
        return BetDTO(
            uuid=bet.uuid,
            user_uuid=bet.user_uuid,
            game_code=bet.game_code,
            amount=bet.amount,
            status=bet.status,
            telegram_transaction_id=bet.telegram_transaction_id,
            created_at=bet.created_at,
            updated_at=bet.updated_at,
        )