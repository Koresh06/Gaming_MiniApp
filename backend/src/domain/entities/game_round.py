from dataclasses import dataclass
from uuid import UUID

from src.domain.entities.base import Entity
from src.domain.exceptions.validation import DomainValidationError
from src.domain.value_object.code_games import GameCode
from src.domain.value_object.outcome_code import OutcomeCode


@dataclass(kw_only=True)
class GameRound(Entity):
    bet_uuid: UUID
    user_uuid: UUID
    game_code: GameCode
    outcome_code: OutcomeCode
    is_win: bool
    win_amount: int
    seed: str

    def __post_init__(self):
        if self.win_amount < 0:
            raise DomainValidationError(message="Сумма выигрыша не может быть отрицательной.")
        if not self.seed:
            raise DomainValidationError(message="Seed не должно быть пустым.")