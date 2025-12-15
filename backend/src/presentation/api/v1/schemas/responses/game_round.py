from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

from src.application.dtos.game_round import GameRoundDTO


class GameRoundResponseSchema(BaseModel):
    uuid: UUID
    bet_uuid: UUID
    user_uuid: UUID
    game_code: str
    outcome_code: str
    is_win: bool
    win_amount: int
    seed: str
    created_at: datetime

    @classmethod
    def from_dto(cls, dto: GameRoundDTO) -> "GameRoundResponseSchema":
        return cls(
            uuid=dto.uuid,
            bet_uuid=dto.bet_uuid,
            user_uuid=dto.user_uuid,
            game_code=dto.game_code.value,
            outcome_code=dto.outcome_code.value,
            is_win=dto.is_win,
            win_amount=dto.win_amount,
            seed=dto.seed,
            created_at=dto.created_at
        )