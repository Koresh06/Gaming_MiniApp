from dataclasses import dataclass, field

from src.domain.entities.base import Entity
from src.domain.exceptions.validation import DomainValidationError
from src.domain.value_object.code_games import GameCode
from src.domain.value_object.outcome_code import OutcomeCode


@dataclass(kw_only=True)
class GameOutcomeSetting(Entity):
    game_code: GameCode
    outcome_code: OutcomeCode
    probability: float = field(default=0.0)
    multiplier: float = field(default=0.0)
    is_active: bool = field(default=True)

    def __post_init__(self):
        if not 0 <= self.probability <= 1:
            raise DomainValidationError(message="Вероятность должна быть 0..1")

        if self.multiplier < 0:
            raise DomainValidationError(message="Множитель должен быть >= 0")
