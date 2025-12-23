from dataclasses import dataclass
from uuid import UUID

from src.domain.value_object.code_games import GameCode
from src.domain.value_object.outcome_code import OutcomeCode


@dataclass(frozen=True, kw_only=True)
class GameResult:
    round_uuid: UUID
    game_code: GameCode
    outcome_code: OutcomeCode
    is_win: bool
    win_amount: int
    payload: dict