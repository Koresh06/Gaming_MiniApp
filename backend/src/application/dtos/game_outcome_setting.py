from uuid import UUID
from dataclasses import dataclass
from datetime import datetime

from src.domain.entities.game_outcome_setting import GameOutcomeSetting
from src.domain.value_object.code_games import GameCode
from src.domain.value_object.outcome_code import OutcomeCode


@dataclass(frozen=True, eq=False, kw_only=True)
class GameOutcomeSettingDTO:
    uuid: UUID
    game_code: GameCode
    outcome_code: OutcomeCode
    probability: float 
    multiplier: float 
    is_active: bool
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, outcome: GameOutcomeSetting) -> "GameOutcomeSettingDTO":
        return GameOutcomeSettingDTO(
            uuid=outcome.uuid,
            game_code=outcome.game_code,
            outcome_code=outcome.outcome_code,
            probability=outcome.probability,
            multiplier=outcome.multiplier,
            is_active=outcome.is_active,
            created_at=outcome.created_at,
            updated_at=outcome.created_at,
        )
    
    def to_entity(self) -> GameOutcomeSetting:
        return GameOutcomeSetting(
            game_code=self.game_code,
            outcome_code=self.outcome_code,
            probability=self.probability,
            multiplier=self.multiplier,
            is_active=self.is_active,
        )
    
@dataclass(frozen=True, eq=False)
class GameOutcomeSettingInputDTO:
    game_code: GameCode
    outcome_code: OutcomeCode
    probability: float
    multiplier: float
    is_active: bool

    def to_entity(self) -> GameOutcomeSetting:
        return GameOutcomeSetting(
            game_code=self.game_code,
            outcome_code=self.outcome_code,
            probability=self.probability,
            multiplier=self.multiplier,
            is_active=self.is_active,
        )