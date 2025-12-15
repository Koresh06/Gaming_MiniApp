from pydantic import BaseModel

from src.application.dtos.game import GameDTO
from src.application.dtos.game_outcome_setting import GameOutcomeSettingDTO


class GameResponseSchema(BaseModel):
    code: str
    name: str

    @classmethod
    def from_dto(cls, dto: GameDTO) -> "GameResponseSchema":
        return cls(**dto.__dict__)


class GameOutcomeSettingResponseSchema(BaseModel):
    outcome_code: str
    probability: float
    multiplier: float
    is_active: bool

    @classmethod
    def from_dto(cls, dto: GameOutcomeSettingDTO) -> "GameOutcomeSettingResponseSchema":
        return cls(
            outcome_code=dto.outcome_code.value,
            probability=dto.probability,
            multiplier=dto.multiplier,
            is_active=dto.is_active,
        )
