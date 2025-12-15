from uuid import UUID
from dataclasses import dataclass
from datetime import datetime

from src.domain.entities.game_round import GameRound
from src.domain.value_object.code_games import GameCode
from src.domain.value_object.outcome_code import OutcomeCode


@dataclass(frozen=True, eq=False, kw_only=True)
class GameRoundDTO:
    uuid: UUID
    bet_uuid: UUID
    user_uuid: UUID
    game_code: GameCode
    outcome_code: OutcomeCode
    is_win: bool
    win_amount: int
    seed: str
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, game_round: GameRound) -> "GameRoundDTO":
        return GameRoundDTO(
            uuid=game_round.uuid,
            bet_uuid=game_round.bet_uuid,
            user_uuid=game_round.user_uuid,
            game_code=game_round.game_code,
            outcome_code=game_round.outcome_code,
            is_win=game_round.is_win,
            win_amount=game_round.win_amount,
            seed=game_round.seed,
            created_at=game_round.created_at,
            updated_at=game_round.updated_at,
        )