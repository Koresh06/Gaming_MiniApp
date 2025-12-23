from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

from src.application.use_cases.game_round.play_game_result import GameResult
from src.application.dtos.game_round import GameRoundDTO


class GameResultResponseSchema(BaseModel):
    round_uuid: UUID
    game_code: str
    outcome_code: str
    is_win: bool
    win_amount: int
    payload: dict

    @classmethod
    def from_dto(cls, dto: GameResult) -> "GameResultResponseSchema":
        return cls(
            round_uuid=dto.round_uuid,
            game_code=dto.game_code.value,
            outcome_code=dto.outcome_code.value,
            is_win=dto.is_win,
            win_amount=dto.win_amount,
            payload=dto.payload,
        )