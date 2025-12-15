from dataclasses import dataclass
from uuid import UUID

from src.domain.entities.base import Entity
from src.domain.exceptions.validation import DomainValidationError
from src.domain.value_object.code_games import GameCode
from src.domain.value_object.bet_status import BetStatus


@dataclass(kw_only=True)
class Bet(Entity):
    user_uuid: UUID
    game_code: GameCode
    amount: int
    status: BetStatus = BetStatus.PENDING
    telegram_transaction_id: str | None = None

    def __post_init__(self):
        if self.amount <= 0:
            raise DomainValidationError(message="Сумма ставки должна быть положительной.")