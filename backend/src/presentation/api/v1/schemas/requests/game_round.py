from uuid import UUID
from pydantic import BaseModel

from src.application.use_cases.game_round.play_game import PlayGameRequest


class PlayGameSchema(BaseModel):
    bet_uuid: UUID

    def to_request(self) -> PlayGameRequest:
        return PlayGameRequest(bet_uuid=self.bet_uuid)
